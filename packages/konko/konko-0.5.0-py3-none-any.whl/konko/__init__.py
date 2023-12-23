from __future__ import annotations

import os

import openai

from .version import VERSION


__version__ = VERSION

_is_legacy_openai = not hasattr(openai, "OpenAI")

if _is_legacy_openai:
    api_base: str | None = None
    base_url: str | None = None
else:
    api_base: type(openai.base_url) = None
    base_url: type(openai.base_url) = None
api_key: str | None = None
openai_api_key: str | None = None


class KonkoError(Exception):
    pass


def _get_base_url() -> str:
    global api_base
    global base_url
    return (
        (api_base and str(api_base))
        or (base_url and str(base_url))
        or os.environ.get(
            "KONKO_BASE_URL",
            os.environ.get("KONKO_API_BASE", "https://api.konko.ai/v1"),
        )
    )


def _get_api_key() -> str:
    global api_key
    value = api_key or os.environ.get("KONKO_API_KEY")
    if not value:
        raise KonkoError(
            "No Konko API key provided."
            "\n\nEither set an environment variable KONKO_API_KEY=<API-KEY> or "
            """set konko.api_key = "<API-KEY>"."""
            "\n\nVisit https://docs.konko.ai/ to request your API key"
        )
    return value


def _get_openai_api_key() -> str | None:
    global openai_api_key
    return openai_api_key or os.environ.get("OPENAI_API_KEY")


if _is_legacy_openai:
    CustomAuthenticationError = KonkoError
    from .chat_completion import ChatCompletion
    from .completion import Completion
    from .model import Model
    from .embedding import Embedding

    def _prepare_kwargs(kwargs):
        if not kwargs.get("api_key"):
            kwargs["api_key"] = _get_api_key()
        if not kwargs.get("api_base"):
            kwargs["api_base"] = _get_base_url()
        openai_api_key = kwargs.get("openai_api_key") or _get_openai_api_key()
        if openai_api_key:
            kwargs["headers"] = {
                **(kwargs.get("headers") or {}),
                "X-OpenAI-Api-Key": openai_api_key,
            }
        return kwargs

    def set_api_base(value: str) -> None:
        global base_url
        global api_base
        base_url = api_base = value

    def set_api_key(value: str) -> None:
        global api_key
        api_key = value

    def set_openai_api_key(value: str) -> None:
        global openai_api_key
        openai_api_key = value

    __all__ = [
        "ChatCompletion",
        "Completion",
        "Embedding",
        "Model",
        "CustomAuthenticationError",
        "KonkoError",
    ]
else:
    import openai.resources
    import openai._utils
    import typing as _t

    def _prepare_kwargs(kwargs: dict[str, _t.Any]) -> dict[str, _t.Any]:
        if not kwargs.get("base_url"):
            kwargs["base_url"] = _get_base_url()
        if not kwargs.get("api_key"):
            kwargs["api_key"] = _get_api_key()
        openai_api_key = kwargs.pop("openai_api_key", None) or _get_openai_api_key()
        if openai_api_key:
            kwargs["default_headers"] = {
                **(kwargs.get("default_headers") or {}),
                "X-OpenAI-Api-Key": openai_api_key,
            }
        return kwargs

    class Konko(openai.OpenAI):
        def __init__(self, **kwargs: _t.Any) -> None:
            kwargs = _prepare_kwargs(kwargs)
            super().__init__(**kwargs)

    class AsyncKonko(openai.AsyncOpenAI):
        def __init__(self, **kwargs: _t.Any) -> None:
            kwargs = _prepare_kwargs(kwargs)
            super().__init__(**kwargs)

    _client: Konko | None = None

    def _load_client() -> Konko:
        global _client
        if _client:
            return _client

        _client = Konko()
        return _client

    def _reset_client() -> None:
        global _client
        if _client:
            _client.close()
        _client = None

    class ChatProxy(openai._utils.LazyProxy[openai.resources.Chat]):
        def __load__(self) -> openai.resources.Chat:
            return _load_client().chat

    class ModelsProxy(openai._utils.LazyProxy[openai.resources.Models]):
        def __load__(self) -> openai.resources.Models:
            return _load_client().models

    class EmbeddingsProxy(openai._utils.LazyProxy[openai.resources.Embeddings]):
        def __load__(self) -> openai.resources.Embeddings:
            return _load_client().embeddings

    class CompletionsProxy(openai._utils.LazyProxy[openai.resources.Completions]):
        def __load__(self) -> openai.resources.Completions:
            return _load_client().completions

    chat: openai.resources.Chat = ChatProxy().__as_proxied__()
    models: openai.resources.Models = ModelsProxy().__as_proxied__()
    embeddings: openai.resources.Embeddings = EmbeddingsProxy().__as_proxied__()
    completions: openai.resources.Completions = CompletionsProxy().__as_proxied__()

    __all__ = [
        "KonkoError",
        "Konko",
        "AsyncKonko",
    ]
