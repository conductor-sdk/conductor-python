from __future__ import annotations

from abc import ABC, abstractmethod


class IntegrationConfig(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class WeviateConfig(IntegrationConfig):

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

    def __init__(self, api_key: str) -> None:
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

    def __init__(self, api_key: str, endpoint: str, classname: str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.classname = classname

    def to_dict(self) -> dict:
        return {
            'api_key': self.api_key,
            'endpoint': self.endpoint
        }
