from typing import List
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.secret_client import SecretClient
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.exceptions.api_exception_handler import api_exception_handler, for_all_methods

@for_all_methods(api_exception_handler, ["__init__"])
class OrkesSecretClient(OrkesBaseClient, SecretClient):
    def __init__(self, configuration: Configuration):
        super(OrkesSecretClient, self).__init__(configuration)

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

