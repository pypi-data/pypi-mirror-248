"""BaseClient for quickly creating typed RPC clients."""
__all__ = ("rpc_client", "rpc_method")

import functools
import inspect
import re
from typing import Any, Callable, ForwardRef, Optional, TypeVar, Union

from pydantic import BaseModel, create_model

# noinspection PyProtectedMember
from pydantic.v1.typing import evaluate_forwardref

from jsonrpc2pyclient.rpcclient import AsyncRPCClient, RPCClient

BaseClient = TypeVar("BaseClient")
FunctionType = TypeVar("FunctionType", bound=Union[Callable])
ClientType = Union[AsyncRPCClient, RPCClient]


def rpc_client(
    transport: ClientType,
    method_prefix: Optional[str] = None,
    method_name_overrides: Optional[dict[str, str]] = None,
) -> Callable[[BaseClient], BaseClient]:
    """Add RPC implementations for the decorated classes methods.

    :param transport: RPC transport client.
    :param method_prefix: Prefix to add to each method name.
    :param method_name_overrides: Map of function name to method name to
        call instead of the `function.__name__`.
    :return: Class wrapper.
    """
    method_name_overrides = method_name_overrides or {}

    def _wrapper(cls: BaseClient) -> BaseClient:
        for attr in dir(cls):
            if callable(getattr(cls, attr)) and not attr.startswith("__"):
                source = inspect.getsource(getattr(cls, attr))
                if re.match(r"^ *(async )?def.*?\.\.\.\n$", source, re.S):
                    name = method_name_overrides.get(attr) or attr
                    setattr(
                        cls,
                        attr,
                        rpc_method(transport, f"{method_prefix}{name}")(
                            getattr(cls, attr)
                        ),
                    )
        return cls

    return _wrapper


def rpc_method(
    transport: ClientType,
    method_name: Optional[str] = None,
) -> Callable[[FunctionType], FunctionType]:
    """Use decorated method signature to call RPC method on call.

    :param transport: RPC transport client.
    :param method_name: Name of the method.
    :return: An implemented version of the decorated method.
    """

    def _decorator(function: FunctionType) -> FunctionType:
        signature = inspect.signature(function)

        # Create model describing method parameters.
        param_model = create_model(  # type: ignore
            f"{function.__name__}Params",
            **{
                k: (
                    resolved_annotation(v.annotation, function),
                    v.default if v.default is not inspect.Signature.empty else ...,
                )
                for k, v in signature.parameters.items()
                if k != "self"
            },
        )

        # Create model describing method result.
        result_model = create_model(
            f"{function.__name__}Result",
            result=(resolved_annotation(signature.return_annotation, function), ...),
        )

        @functools.wraps(function)
        async def _wrapper(*args: Any, **kwargs: Any) -> Any:
            params_dict, transport_kwargs = _parse_params(param_model, *args, **kwargs)
            params = params_dict if kwargs else list(params_dict.values())
            name = method_name if method_name is not None else function.__name__
            # Type ignore because mypy is wrong.
            response = await transport.call(
                name, params, **transport_kwargs  # type: ignore
            )
            # Cast to proper return type.
            # Type ignore because mypy can't understand `create_model`.
            return result_model(result=response).result  # type: ignore

        return _wrapper  # type: ignore

    return _decorator


def resolved_annotation(annotation: Any, function: Callable) -> Any:
    """Get annotation resolved."""
    if annotation == inspect.Signature.empty:
        return Any
    globalns = getattr(function, "__globals__", {})
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return type(None) if annotation is None else annotation


def _parse_params(
    params_model: BaseModel, *args: Any, **kwargs: Any
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Get method params and transport kwargs.

    :param params_model: Model describing method parameters.
    :param args: Args passed to method call.
    :param kwargs: Keyword args passed to method call.
    :return: A tuple of method params, transport kwargs.
    """
    params = {}
    transport_kwargs = {}
    param_names = list(params_model.model_fields.keys())

    # Get params passed by position.
    for i, arg in enumerate(args):
        # Offset by 1 to skip `self` arg.
        if i == 0:
            continue
        params[param_names[i - 1]] = arg

    # Get params passed by name.
    for name, arg in kwargs.items():
        if name in param_names:
            params[name] = arg
        else:
            # If not in param names must be transport arg.
            transport_kwargs[name] = arg
    if params:
        params = params_model.model_validate(params).model_dump(exclude_unset=True)
    return params, transport_kwargs
