from openai.api_resources.completion import Completion as _Completion


class Completion(_Completion):
    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new completion for the provided prompt and parameters.

        See https://docs.konko.ai/reference/createcompletion for a list
        of valid parameters.
        """
        from . import _prepare_kwargs

        kwargs = _prepare_kwargs(kwargs)
        return super().create(*args, **kwargs)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        """
        Creates a new completion for the provided prompt and parameters.

        See https://docs.konko.ai/reference/createcompletion for a list
        of valid parameters.
        """
        from . import _prepare_kwargs

        kwargs = _prepare_kwargs(kwargs)
        return super().create(*args, **kwargs)
