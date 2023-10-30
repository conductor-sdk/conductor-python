from typing import List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.secret_resource_api import SecretResourceApi
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.interfaces.secret_client_interface import SecretClientInterface

class SecretClient(SecretClientInterface):
    def __init__(self, configuration: Configuration):
        api_client = ApiClient(configuration)
        self.secretResourceApi = SecretResourceApi(api_client)

    def putSecret(self, key: str, value: str):
        self.secretResourceApi.put_secret(value, key)
    
    def getSecret(self, key: str) -> str:
        return self.secretResourceApi.get_secret(key)
    
    def listAllSecretNames(self) -> set[str]:
        return set(self.secretResourceApi.list_all_secret_names())
    
    def listSecretsThatUserCanGrantAccessTo(self) -> List[str]:
        return self.secretResourceApi.list_secrets_that_user_can_grant_access_to()

    def deleteSecret(self, key: str):
        self.secretResourceApi.delete_secret(key)

    def secretExists(self, key: str) -> bool:
        return self.secretResourceApi.secret_exists(key)
    
    def setSecretTags(self, tags: List[MetadataTag], key: str):
        self.secretResourceApi.put_tag_for_secret(tags, key)

    def getSecretTags(self, key: str) -> List[MetadataTag]:
        return self.secretResourceApi.get_tags(key)
        
    def deleteSecretTags(self, tags: List[MetadataTag], key: str) -> List[MetadataTag]:
        self.secretResourceApi.delete_tag_for_secret(tags, key)

