from __future__ import absolute_import
from abc import ABC, abstractmethod


class IntegrationClient(ABC):
    """Client for managing integrations with external systems.  Some examples of integrations are:
    1. AI/LLM providers (e.g. OpenAI, HuggingFace)
    2. Vector DBs (Pinecone, Weaviate etc.)
    3. Kafka
    4. Relational databases

    Integrations are configured as integration -> api with 1->N cardinality.
    APIs are the underlying resources for an integration and depending on the type of integration they represent underlying resources.
    Examples:
        LLM integrations
        The integration specifies the name of the integration unique to your environment, api keys and endpoint used.
        APIs are the models (e.g. text-davinci-003, or text-embedding-ada-002)

        Vector DB integrations,
        The integration represents the cluster, specifies the name of the integration unique to your environment, api keys and endpoint used.
        APIs are the indexes (e.g. pinecone) or class (e.g. for weaviate)

        Kafka
        The integration represents the cluster, specifies the name of the integration unique to your environment, api keys and endpoint used.
        APIs are the topics that are configured for use within this kafka cluster
    """

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
