from __future__ import annotations

import os
from abc import ABC, abstractmethod


class IntegrationConfig(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class WeaviateConfig(IntegrationConfig):

    def __init__(self, api_key: str, endpoint: str, classname: str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.classname = classname

    def to_dict(self) -> dict:
        return {
            'api_key': self.api_key,
            'endpoint': self.endpoint
        }


class OpenAIConfig(IntegrationConfig):

    def __init__(self, api_key: str = None) -> None:
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        self.api_key = api_key

    def to_dict(self) -> dict:
        return {
            'api_key': self.api_key
        }


class AzureOpenAIConfig(IntegrationConfig):

    def __init__(self, api_key: str, endpoint: str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint

    def to_dict(self) -> dict:
        return {
            'api_key': self.api_key,
            'endpoint': self.endpoint
        }


class PineconeConfig(IntegrationConfig):

    def __init__(self, api_key: str, endpoint: str, environment: str, project_name: str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.environment = environment
        self.project_name = project_name

    def to_dict(self) -> dict:
        return {
            'api_key': self.api_key,
            'endpoint': self.endpoint,
            'projectName': self.project_name,
            'environment': self.environment
        }
