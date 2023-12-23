from openai.api_resources.chat_completion import ChatCompletion as _ChatCompletion


class ChatCompletion(_ChatCompletion):
    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new chat completion for the provided messages and paramaters.

        See https://docs.konko.ai/reference/createchatcompletion
        for a list of valid parameters.
        """
        from . import _prepare_kwargs

        kwargs = _prepare_kwargs(kwargs)
        return super().create(*args, **kwargs)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        """
        Creates a new chat completion for the provided messages and paramaters.

        See https://docs.konko.ai/reference/createchatcompletion
        for a list of valid parameters.
        """
        from . import _prepare_kwargs

        kwargs = _prepare_kwargs(kwargs)
        return await super().acreate(*args, **kwargs)
