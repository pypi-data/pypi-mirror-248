"""RPCClient abstract classes for sync and async RPC clients."""
import abc
import inspect
from typing import Any, Optional, Union

from jsonrpc2pyclient._irpcclient import IRPCClient

__all__ = ("AsyncRPCClient", "RPCClient")


class AsyncRPCClient(abc.ABC, IRPCClient):
    """Abstract class for creating async JSON-RPC clients."""

    @abc.abstractmethod
    async def _send_and_get_json(
        self, request_json: str, request_id: int, **kwargs: Any
    ) -> Union[bytes, str, dict[str, Any]]:
        ...

    async def call(
        self,
        method: str,
        params: Optional[Union[list[Any], dict[str, Any]]] = None,
        **kwargs: Any
    ) -> Any:
        """Call a method with the provided params.

        :param method: Method to call.
        :param params: Params to pass to called method.
        :param kwargs: Arguments to pass to transport implementation.
        :return: The method call result or error.
        """
        for hook in self.pre_call_hooks:
            await hook() if inspect.iscoroutinefunction(hook) else hook()
        request = self._build_request(method, params)
        # Type ignore because id will always be `int` because this
        # client creates the id.
        data = await self._send_and_get_json(
            request.model_dump_json(by_alias=True), request.id, **kwargs  # type: ignore
        )
        return self._get_result_from_response(data)


class RPCClient(abc.ABC, IRPCClient):
    """Abstract class for creating a JSON-RPC clients."""

    @abc.abstractmethod
    def _send_and_get_json(
        self, request_json: str, request_id: int, **kwargs: Any
    ) -> Union[bytes, str, dict[str, Any]]:
        ...

    def call(
        self,
        method: str,
        params: Optional[Union[list[Any], dict[str, Any]]] = None,
        **kwargs: Any
    ) -> Any:
        """Call a method with the provided params.

        :param method: Method to call.
        :param params: Params to pass to called method.
        :param kwargs: Arguments to pass to transport implementation.
        :return: The method call result or error.
        """
        request = self._build_request(method, params)
        for hook in self.pre_call_hooks:
            hook()
        # Type ignore because id will always be `int` because this
        # client creates the id.
        return self._get_result_from_response(
            self._send_and_get_json(
                request.model_dump_json(by_alias=True),
                request.id,  # type: ignore
                **kwargs
            )
        )
