from __future__ import absolute_import

import re  # noqa: F401
from abc import ABC, abstractmethod
from typing import List

# python 2 and python 3 compatibility library
import six

from conductor.client.http.api_client import ApiClient
from conductor.client.http.models.prompt import Prompt
from conductor.client.orkes.models.metadata_tag import MetadataTag


class PromptClient(ABC):

    @abstractmethod
    def save_prompt(self, prompt_name: str, description: str, prompt: Prompt):
        pass

    @abstractmethod
    def get_prompt(self, prompt_name: str) -> Prompt:
        pass

    @abstractmethod
    def get_prompts(self):
        pass

    @abstractmethod
    def delete_prompt(self, prompt_name: str):
        pass

    @abstractmethod
    def get_tags_for_prompt_template(self, prompt_name: str) -> List[MetadataTag]:
        pass

    @abstractmethod
    def update_tag_for_prompt_template(self, prompt_name: str, tags: List[MetadataTag]):
        pass

    @abstractmethod
    def delete_tag_for_prompt_template(self, prompt_name: str, tags: List[MetadataTag]):
        pass
