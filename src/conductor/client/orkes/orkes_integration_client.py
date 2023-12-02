from __future__ import absolute_import
from abc import ABC, abstractmethod

from conductor.client.configuration.configuration import Configuration
from conductor.client.integration_client import IntegrationClient
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.exceptions.api_exception_handler import api_exception_handler, for_all_methods


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesIntegrationClient(OrkesBaseClient, IntegrationClient):

    def __init__(self, configuration: Configuration):
        super(OrkesIntegrationClient, self).__init__(configuration)

    @abstractmethod
    def associate_prompt_with_integration(self, ai_integration, model_name, prompt_name):
        """Associate a prompt with an AI integration and model"""
        pass

    @abstractmethod
    def delete_integration_api(self, api_name, integration_name):
        """Delete a specific integration api for a given integration"""
        pass

    def delete_integration(self, integration_name):
        """Delete an integration"""
        pass

    def get_integration_api(self, name, integration_name):
        pass

    def get_integration_apis(self, name):
        pass

    def get_integration_available_apis(self, name):
        pass

    def get_integration_provider(self, name):
        pass

    def get_integration_provider_defs(self):
        pass

    def get_integration_providers(self):
        pass

    def get_prompts_with_integration(self, integration_provider, integration_name):
        pass

    def get_providers_and_integrations(self):
        pass

    def get_token_usage_for_integration(self, name, integration_name):
        pass

    def get_token_usage_for_integration_provider(self, name):
        pass

    def register_token_usage(self, body, name, integration_name):
        pass

    def save_integration_api(self, body, name, integration_name):
        pass

    def save_integration_provider(self, body, name):
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
