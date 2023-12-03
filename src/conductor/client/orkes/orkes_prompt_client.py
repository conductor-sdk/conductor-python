from __future__ import absolute_import

import re  # noqa: F401
from abc import ABC, abstractmethod
from typing import List

# python 2 and python 3 compatibility library
import six

from conductor.client.configuration.configuration import Configuration
from conductor.client.exceptions.api_exception_handler import api_exception_handler, for_all_methods
from conductor.client.http.api_client import ApiClient
from conductor.client.http.models.prompt import Prompt
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.prompt_client import PromptClient


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesPromptClient(OrkesBaseClient, PromptClient):

    def __init__(self, configuration: Configuration):
        super(PromptClient, self).__init__(configuration)

    @abstractmethod
    def save_prompt(self, prompt_name: str, description: str, prompt: Prompt):
        self.promptApi.save_message_template(prompt, description, prompt_name)

    @abstractmethod
    def get_prompt(self, prompt_name: str) -> Prompt:
        return self.promptApi.get_message_template(prompt_name)

    @abstractmethod
    def get_prompts(self):
        return self.promptApi.get_message_templates()

    @abstractmethod
    def delete_prompt(self, prompt_name: str):
        self.promptApi.delete_message_template(prompt_name)

    @abstractmethod
    def get_tags_for_prompt_template(self, prompt_name: str) -> List[MetadataTag]:
        self.promptApi.get_tags_for_prompt_template(prompt_name)

    @abstractmethod
    def update_tag_for_prompt_template(self, prompt_name: str, tags: List[MetadataTag]):
        self.promptApi.put_tag_for_prompt_template(tags, prompt_name)

    @abstractmethod
    def delete_tag_for_prompt_template(self, prompt_name: str, tags: List[MetadataTag]):
        self.promptApi.delete_tag_for_prompt_template(tags, prompt_name)
