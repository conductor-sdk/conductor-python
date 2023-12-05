"""Orkes Secret Client

The class in this module allows management of secrets.
"""

from typing import List

from conductor.client.exceptions.api_exception_handler import (
    api_exception_handler, for_all_methods)
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.secret_client import SecretClient


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesSecretClient(OrkesBaseClient, SecretClient):
    """
    A class to manage Orkes secrets including secret tag management.
    """

    def put_secret(self, key: str, value: str):
        self.secret_resource_api.put_secret(value, key)

    def get_secret(self, key: str) -> str:
        return self.secret_resource_api.get_secret(key)

    def list_all_secret_names(self) -> set[str]:
        return set(self.secret_resource_api.list_all_secret_names())

    def list_secrets_that_user_can_grant_access_to(self) -> List[str]:
        return self.secret_resource_api.list_secrets_that_user_can_grant_access_to()

    def delete_secret(self, key: str):
        self.secret_resource_api.delete_secret(key)

    def secret_exists(self, key: str) -> bool:
        return self.secret_resource_api.secret_exists(key)

    def set_secret_tags(self, tags: List[MetadataTag], key: str):
        self.secret_resource_api.put_tag_for_secret(tags, key)

    def get_secret_tags(self, key: str) -> List[MetadataTag]:
        return self.secret_resource_api.get_tags(key)

    def delete_secret_tags(
        self, tags: List[MetadataTag], key: str
    ) -> List[MetadataTag]:
        self.secret_resource_api.delete_tag_for_secret(tags, key)
