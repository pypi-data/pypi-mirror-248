from openai.api_resources.model import Model as _Model
import openai.util as util


class Model(_Model):
    @classmethod
    def list(cls, **kwargs):
        from . import _prepare_kwargs

        kwargs = _prepare_kwargs(kwargs)

        request_id = kwargs.pop("request_id", None)
        api_key = kwargs.pop("api_key", None)
        api_version = kwargs.pop("api_version", None)
        organization = kwargs.pop("organization", None)
        api_base = kwargs.pop("api_base", None)
        api_type = kwargs.pop("api_type", None)
        headers = kwargs.pop("headers", None)

        requestor, url = cls._ListableAPIResource__prepare_list_requestor(
            api_key,
            api_version,
            organization,
            api_base,
            api_type,
        )

        response, _, api_key = requestor.request(
            "get", url, kwargs, headers=headers, request_id=request_id
        )
        openai_object = util.convert_to_openai_object(
            response, api_key, api_version, organization
        )
        openai_object._retrieve_params = kwargs
        return openai_object

    @classmethod
    async def alist(cls, **kwargs):
        from . import _prepare_kwargs

        kwargs = _prepare_kwargs(kwargs)

        request_id = kwargs.pop("request_id", None)
        api_key = kwargs.pop("api_key", None)
        api_version = kwargs.pop("api_version", None)
        organization = kwargs.pop("organization", None)
        api_base = kwargs.pop("api_base", None)
        api_type = kwargs.pop("api_type", None)
        headers = kwargs.pop("headers", None)

        requestor, url = cls._ListableAPIResource__prepare_list_requestor(
            api_key,
            api_version,
            organization,
            api_base,
            api_type,
        )

        response, _, api_key = await requestor.arequest(
            "get", url, kwargs, headers=headers, request_id=request_id
        )
        openai_object = util.convert_to_openai_object(
            response, api_key, api_version, organization
        )
        openai_object._retrieve_params = kwargs
        return openai_object
