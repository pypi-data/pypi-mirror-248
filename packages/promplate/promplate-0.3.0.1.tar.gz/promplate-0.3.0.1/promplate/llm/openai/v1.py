from copy import copy
from functools import cached_property
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Callable, ParamSpec, TypeVar

from openai import AsyncClient, Client  # type: ignore

from ...prompt.chat import Message, ensure
from ..base import *

P = ParamSpec("P")
T = TypeVar("T")


def same_params_as(_: Callable[P, Any]):
    def func(__init__: Callable[..., None]) -> Callable[P, None]:
        return __init__  # type: ignore

    return func


class Config(Configurable):
    def __init__(self, **config):
        super().__init__(**config)
        self._run_config = {}

    def bind(self, **run_config):
        obj = copy(self)
        obj._run_config = self._run_config | run_config
        return obj

    @property
    def _config(self):  # type: ignore
        return MappingProxyType(super()._config)

    @cached_property
    def client(self):
        return Client(**self._config)

    @cached_property
    def aclient(self):
        return AsyncClient(**self._config)


if TYPE_CHECKING:

    class ClientConfig(Config):
        @same_params_as(Client)
        def __init__(self, **config):
            ...

    class AsyncClientConfig(Config):
        @same_params_as(AsyncClient)
        def __init__(self, **config):
            ...

else:
    ClientConfig = AsyncClientConfig = Config


class TextComplete(ClientConfig):
    def __call__(self, text: str, /, **config):
        config = self._run_config | config | {"stream": False, "prompt": text}
        result = self.client.completions.create(**config)
        return result.choices[0].text


class AsyncTextComplete(AsyncClientConfig):
    async def __call__(self, text: str, /, **config):
        config = self._run_config | config | {"stream": False, "prompt": text}
        result = await self.aclient.completions.create(**config)
        return result.choices[0].text


class TextGenerate(ClientConfig):
    def __call__(self, text: str, /, **config):
        config = self._run_config | config | {"stream": True, "prompt": text}
        stream = self.client.completions.create(**config)
        for event in stream:
            yield event.choices[0].text


class AsyncTextGenerate(AsyncClientConfig):
    async def __call__(self, text: str, /, **config):
        config = self._run_config | config | {"stream": True, "prompt": text}
        stream = await self.aclient.completions.create(**config)
        async for event in stream:
            yield event.choices[0].text


class ChatComplete(ClientConfig):
    def __call__(self, messages: list[Message] | str, /, **config):
        messages = ensure(messages)
        config = self._run_config | config | {"stream": False, "messages": messages}
        result = self.client.chat.completions.create(**config)
        return result.choices[0].message.content


class AsyncChatComplete(AsyncClientConfig):
    async def __call__(self, messages: list[Message] | str, /, **config):
        messages = ensure(messages)
        config = self._run_config | config | {"stream": False, "messages": messages}
        result = await self.aclient.chat.completions.create(**config)
        return result.choices[0].message.content


class ChatGenerate(ClientConfig):
    def __call__(self, messages: list[Message] | str, /, **config):
        messages = ensure(messages)
        config = self._run_config | config | {"stream": True, "messages": messages}
        stream = self.client.chat.completions.create(**config)
        for event in stream:
            yield event.choices[0].delta.content or ""


class AsyncChatGenerate(AsyncClientConfig):
    async def __call__(self, messages: list[Message] | str, /, **config):
        messages = ensure(messages)
        config = self._run_config | config | {"stream": True, "messages": messages}
        stream = await self.aclient.chat.completions.create(**config)
        async for event in stream:
            yield event.choices[0].delta.content or ""


class SyncTextOpenAI(ClientConfig, LLM):
    complete = TextComplete.__call__  # type: ignore
    generate = TextGenerate.__call__  # type: ignore


class AsyncTextOpenAI(AsyncClientConfig, LLM):
    complete = AsyncTextComplete.__call__  # type: ignore
    generate = AsyncTextGenerate.__call__  # type: ignore


class SyncChatOpenAI(ClientConfig, LLM):
    complete = ChatComplete.__call__  # type: ignore
    generate = ChatGenerate.__call__  # type: ignore


class AsyncChatOpenAI(AsyncClientConfig, LLM):
    complete = AsyncChatComplete.__call__  # type: ignore
    generate = AsyncChatGenerate.__call__  # type: ignore
