"""Orkes Integration Client

The class in this module allows management of integrations supported by Orkes.
"""

from __future__ import absolute_import

from typing import List

from conductor.client.exceptions.api_exception_handler import (
    api_exception_handler, for_all_methods)
from conductor.client.http.models.integration import Integration
from conductor.client.http.models.integration_api import IntegrationApi
from conductor.client.http.models.integration_api_update import \
    IntegrationApiUpdate
from conductor.client.http.models.integration_update import IntegrationUpdate
from conductor.client.http.models.prompt_template import PromptTemplate
from conductor.client.integration_client import IntegrationClient
from conductor.client.orkes.orkes_base_client import OrkesBaseClient


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesIntegrationClient(OrkesBaseClient, IntegrationClient):
    """
    A class to manage integration providers, integrations, integration related
    prompts, tokens and tags.
    """

    def associate_prompt_with_integration(
        self, ai_integration: str, model_name: str, prompt_name: str
    ):
        self.integration_api.associate_prompt_with_integration(
            ai_integration, model_name, prompt_name
        )

    def delete_integration_api(self, api_name: str, integration_name: str):
        self.integration_api.delete_integration_api(api_name, integration_name)

    def delete_integration(self, integration_name: str):
        self.integration_api.delete_integration_provider(integration_name)

    def get_integration_api(
        self, api_name: str, integration_name: str
    ) -> IntegrationApi:
        return self.integration_api.get_integration_api(api_name, integration_name)

    def get_integration_apis(self, integration_name: str) -> List[IntegrationApi]:
        return self.integration_api.get_integration_apis(integration_name)

    def get_integration(self, integration_name: str) -> Integration:
        return self.integration_api.get_integration_provider(integration_name)

    def get_integrations(self) -> List[Integration]:
        return self.integration_api.get_integration_providers()

    def get_prompts_with_integration(
        self, ai_integration: str, model_name: str
    ) -> List[PromptTemplate]:
        return self.integration_api.get_prompts_with_integration(
            ai_integration, model_name
        )

    def save_integration_api(
        self, integration_name, api_name, api_details: IntegrationApiUpdate
    ):
        self.integration_api.save_integration_api(
            api_details, integration_name, api_name
        )

    def save_integration(
        self, integration_name, integration_details: IntegrationUpdate
    ):
        self.integration_api.save_integration_provider(
            integration_details, integration_name
        )

    def get_token_usage_for_integration(self, name, integration_name) -> int:
        return self.integration_api.get_token_usage_for_integration(
            name, integration_name
        )

    def get_token_usage_for_integration_provider(self, name) -> dict:
        return self.integration_api.get_token_usage_for_integration_provider(name)

    def register_token_usage(self, body, name, integration_name):
        pass

    # Tags

    def delete_tag_for_integration(self, body, tag_name, integration_name):
        """Delete an integration"""
        pass

    def delete_tag_for_integration_provider(self, body, name):
        pass

    def put_tag_for_integration(self, body, name, integration_name):
        pass

    def put_tag_for_integration_provider(self, body, name):
        pass

    def get_tags_for_integration(self, name, integration_name):
        pass

    def get_tags_for_integration_provider(self, name):
        pass
