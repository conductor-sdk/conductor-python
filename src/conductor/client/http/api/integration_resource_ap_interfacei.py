from __future__ import absolute_import

import re  # noqa: F401


class IntegrationResourceApi(object):
    def associate_prompt_with_integration(self, integration_provider, integration_name, prompt_name,
                                          **kwargs):  # noqa: E501
        pass

    def delete_integration_api(self, name, integration_name, **kwargs):  # noqa: E501
        pass

    def delete_integration_provider(self, name, **kwargs):  # noqa: E501
        pass

    def delete_tag_for_integration(self, body, name, integration_name, **kwargs):  # noqa: E501
        pass

    def delete_tag_for_integration_provider(self, body, name, **kwargs):  # noqa: E501
        pass

    def get_integration_api(self, name, integration_name, **kwargs):  # noqa: E501
        pass

    def get_integration_apis(self, name, **kwargs):  # noqa: E501
        pass

    def get_integration_available_apis(self, name, **kwargs):  # noqa: E501
        pass

    def get_integration_provider(self, name, **kwargs):  # noqa: E501
        pass

    def get_integration_provider_defs(self, **kwargs):  # noqa: E501
        pass

    def get_integration_providers(self, **kwargs):  # noqa: E501
        pass

    def get_prompts_with_integration(self, integration_provider, integration_name, **kwargs):  # noqa: E501
        pass

    def get_providers_and_integrations(self, **kwargs):  # noqa: E501
        pass

    def get_tags_for_integration(self, name, integration_name, **kwargs):  # noqa: E501
        pass

    def get_tags_for_integration_provider(self, name, **kwargs):  # noqa: E501
        pass

    def get_token_usage_for_integration(self, name, integration_name, **kwargs):  # noqa: E501
        pass

    def get_token_usage_for_integration_provider(self, name, **kwargs):  # noqa: E501
        pass

    def put_tag_for_integration(self, body, name, integration_name, **kwargs):  # noqa: E501
        pass

    def put_tag_for_integration_provider(self, body, name, **kwargs):  # noqa: E501
        pass

    def register_token_usage(self, body, name, integration_name, **kwargs):  # noqa: E501
        pass

    def save_integration_api(self, body, name, integration_name, **kwargs):  # noqa: E501
        pass

    def save_integration_provider(self, body, name, **kwargs):  # noqa: E501
        pass
