import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.event_resource_api import EventResourceApi
from conductor.client.http.models.event_handler import EventHandler
from conductor.client.interfaces.event_client_interface import EventClientInterface

class EventClient(EventClientInterface):
    def __init__(self, configuration: Configuration):
        api_client = ApiClient(configuration)
        self.eventResourceApi = EventResourceApi(api_client)

    def registerEventHandler(self, eventHandler: EventHandler):
        self.eventResourceApi.add_event_handler(eventHandler)
    
    def updateEventHandler(self, eventHandler: EventHandler):
        self.eventResourceApi.update_event_handler(eventHandler)

    def getEventHandlers(self, event: str, activeOnly: Optional[bool] = True) -> List[EventHandler]:
        return self.eventResourceApi.get_event_handlers_for_event(event, active_only=activeOnly)

    def unregisterEventHandler(self, name: str):
        self.eventResourceApi.remove_event_handler_status(name)

    def putQueueConfig(self, queueType: str, queueName: str, config: object):
        self.eventResourceApi.put_queue_config(json.dumps(config), queueType, queueName)
            
    def getQueueConfig(self, queueType: str, queueName: str) -> Dict[str, object]:
        return self.eventResourceApi.get_queue_config(queueType, queueName)

    def deleteQueueConfig(self, queueType: str, queueName: str):
        self.eventResourceApi.delete_queue_config(queueType, queueName)