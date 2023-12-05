"""Orkes Prompt Client

The class in this module allows management of Orkes AI Prompts.
"""

from __future__ import absolute_import

from typing import List

from conductor.client.exceptions.api_exception_handler import (
    api_exception_handler, for_all_methods)
from conductor.client.http.models.prompt_template import PromptTemplate
from conductor.client.http.models.prompt_test_request import \
    PromptTemplateTestRequest
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.prompt_client import PromptClient


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesPromptClient(OrkesBaseClient, PromptClient):
    """
    A class to manage AI Prompts. Supports creating prompts, testing of prompts
    and prompt tag management.
    """

    def save_prompt(self, prompt_name: str, description: str, prompt_template: str):
        self.prompt_api.save_message_template(prompt_template, description, prompt_name)

    def get_prompt(self, prompt_name: str) -> PromptTemplate:
        return self.prompt_api.get_message_template(prompt_name)

    def get_prompts(self):
        return self.prompt_api.get_message_templates()

    def delete_prompt(self, prompt_name: str):
        self.prompt_api.delete_message_template(prompt_name)

    def get_tags_for_prompt_template(self, prompt_name: str) -> List[MetadataTag]:
        self.prompt_api.get_tags_for_prompt_template(prompt_name)

    def update_tag_for_prompt_template(self, prompt_name: str, tags: List[MetadataTag]):
        self.prompt_api.put_tag_for_prompt_template(tags, prompt_name)

    def delete_tag_for_prompt_template(self, prompt_name: str, tags: List[MetadataTag]):
        self.prompt_api.delete_tag_for_prompt_template(tags, prompt_name)

    def test_prompt(
        self,
        prompt_text: str,
        variables: dict,
        ai_integration: str,
        text_complete_model: str,
        temperature: float = 0.1,
        top_p: float = 0.9,
        stop_words: List[str] = None,
    ) -> str:
        request = PromptTemplateTestRequest()
        request.prompt = prompt_text
        request.llm_provider = ai_integration
        request.model = text_complete_model
        request.prompt_variables = variables
        request.temperature = temperature
        request.top_p = top_p
        if stop_words is not None:
            request.stop_words = stop_words
        return self.prompt_api.test_message_template(request)
