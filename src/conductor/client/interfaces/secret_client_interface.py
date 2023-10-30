from abc import ABC, abstractmethod
from typing import List
from conductor.client.orkes.models.metadata_tag import MetadataTag

class SecretClientInterface(ABC):
    @abstractmethod
    def putSecret(self, key: str, value: str):
        pass
    
    @abstractmethod
    def getSecret(self, key: str) -> str:
        pass
    
    @abstractmethod
    def listAllSecretNames(self) -> set[str]:
        pass
    
    @abstractmethod
    def listSecretsThatUserCanGrantAccessTo(self) -> List[str]:
        pass

    @abstractmethod
    def deleteSecret(self, key: str):
        pass

    @abstractmethod
    def secretExists(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def setSecretTags(self, tags: List[MetadataTag], key: str):
        pass

    @abstractmethod
    def getSecretTags(self, key: str) -> List[MetadataTag]:
        pass
        
    @abstractmethod
    def deleteSecretTags(self, tags: List[MetadataTag], key: str) -> List[MetadataTag]:
        pass

