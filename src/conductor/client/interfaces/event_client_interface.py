from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from conductor.client.http.models.event_handler import EventHandler

class EventClientInterface(ABC):
    @abstractmethod
    def registerEventHandler(self, eventHandler: EventHandler):
        pass
    
    @abstractmethod
    def updateEventHandler(self, eventHandler: EventHandler):
        pass

    @abstractmethod
    def getEventHandlers(self, event: str, activeOnly: Optional[bool] = True) -> List[EventHandler]:
        pass

    @abstractmethod
    def unregisterEventHandler(self, name: str):
        pass
    
    @abstractmethod
    def putQueueConfig(self, queueType: str, queueName: str, config: object):
        pass

    @abstractmethod
    def getQueueConfig(self, queueType: str, queueName: str) -> Dict[str, object]:
        pass
        
    @abstractmethod
    def deleteQueueConfig(self, queueType: str, queueName: str):
        pass

