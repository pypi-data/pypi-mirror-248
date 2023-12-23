from openai.api_resources.embedding import Embedding as _Embedding


class Embedding(_Embedding):
    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new embedding for the provided input and parameters.

        See https://docs.konko.ai/reference/post_embeddings for a list
        of valid parameters.
        """
        from . import _prepare_kwargs

        kwargs = _prepare_kwargs(kwargs)
        return super().create(*args, **kwargs)

    @classmethod
    async def acreate(cls, *args, **kwargs):
        """
        Creates a new embedding for the provided input and parameters.

        See https://docs.konko.ai/reference/post_embeddings for a list
        of valid parameters.
        """
        from . import _prepare_kwargs

        kwargs = _prepare_kwargs(kwargs)
        return super().acreate(*args, **kwargs)
