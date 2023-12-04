from __future__ import annotations

import time
from typing import List, Optional
from uuid import uuid4

from typing_extensions import Self

from conductor.client.ai.configuration import LLMProvider, VectorDB
from conductor.client.ai.integrations import IntegrationConfig
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.integration_api_update import IntegrationApiUpdate
from conductor.client.http.models.integration_update import IntegrationUpdate
from conductor.client.orkes_clients import OrkesClients


class AIOrchestrator:
    def __init__(
        self, api_configuration: Configuration, prompt_test_workflow_name: str = ""
    ) -> Self:
        orkes_clients = OrkesClients(api_configuration)

        self.integration_client = orkes_clients.get_integration_client()
        self.workflow_client = orkes_clients.get_integration_client()
        self.workflow_executor = orkes_clients.get_workflow_executor()
        self.prompt_client = orkes_clients.get_prompt_client()

        self.prompt_test_workflow_name = prompt_test_workflow_name
        if self.prompt_test_workflow_name == "":
            self.prompt_test_workflow_name = "prompt_test_" + str(uuid4())

    def add_prompt_template(self, name: str, prompt_template: str, description: str):
        self.prompt_client.save_prompt(name, description, prompt_template)
        return self

    def associate_prompt_template(
        self, name: str, ai_integration: str, ai_models: List[str]
    ):
        for ai_model in ai_models:
            self.integration_client.associate_prompt_with_integration(
                ai_integration, ai_model, name
            )

    def test_prompt_template(
        self,
        text: str,
        variables: dict,
        ai_integration: str,
        text_complete_model: str,
        stop_words: Optional[List[str]] = [],
        max_tokens: Optional[int] = 100,
        temperature: int = 0,
        top_p: int = 1,
    ):
        return self.prompt_client.test_prompt(
            text,
            variables,
            ai_integration,
            text_complete_model,
            temperature,
            top_p,
            stop_words,
        )

    def add_ai_integration(
        self,
        ai_integration_name: str,
        provider: LLMProvider,
        models: List[str],
        description: str,
        config: IntegrationConfig,
    ):
        details = IntegrationUpdate()
        details.configuration = config.to_dict()
        details.type = provider.value
        details.category = "AI_MODEL"
        details.enabled = True
        details.description = description
        self.integration_client.save_integration(ai_integration_name, details)
        for model in models:
            api_details = IntegrationApiUpdate()
            api_details.enabled = True
            api_details.description = description
            self.integration_client.save_integration_api(
                ai_integration_name, model, api_details
            )

    def add_vector_store(
        self,
        name: str,
        provider: VectorDB,
        indices: List[str],
        description: str,
        config: IntegrationConfig,
    ):
        vector_db = IntegrationUpdate()
        vector_db.configuration = config.to_dict()
        vector_db.type = provider.value
        vector_db.category = "VECTOR_DB"
        vector_db.enabled = True
        vector_db.description = description
        self.integration_client.save_integration(name, vector_db)
        for index in indices:
            api_details = IntegrationApiUpdate()
            api_details.enabled = True
            api_details.description = description
            self.integration_client.save_integration_api(name, index, api_details)
        pass

    def get_token_used(self, ai_integration: str) -> dict:
        return self.integration_client.get_token_usage_for_integration_provider(
            ai_integration
        )

    def get_token_used_by_model(self, ai_integration: str, model: str) -> int:
        return self.integration_client.get_token_usage_for_integration(
            ai_integration, model
        )
