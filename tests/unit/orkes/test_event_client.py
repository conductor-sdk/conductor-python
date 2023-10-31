import logging
import unittest

from unittest.mock import Mock, patch, MagicMock
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.orkes_event_client import OrkesEventClient
from conductor.client.http.api.event_resource_api import EventResourceApi
from conductor.client.http.models.event_handler import EventHandler

EVENT_NAME = 'ut_event'
EVENT_HANDLER_1_NAME = 'ut_event_handler_1_name'
EVENT_HANDLER_2_NAME = 'ut_event_handler_2_name'
QUEUE_TYPE = 'kafka'
QUEUE_NAME = 'topic_0'
ERROR_BODY= '{"message":"No such event found by key"}'

class TestOrkesEventClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.event_client = OrkesEventClient(configuration)
        cls.event_handlers = [
            EventHandler(name=EVENT_HANDLER_1_NAME, event=EVENT_NAME, active=True),
            EventHandler(name=EVENT_HANDLER_2_NAME, event=EVENT_NAME, active=False)
        ]
        
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "eventResourceApi is not of type EventResourceApi"
        self.assertIsInstance(self.event_client.eventResourceApi, EventResourceApi, message)

    @patch.object(EventResourceApi, 'add_event_handler')
    def test_registerEventHandler(self, mock):
        self.event_client.registerEventHandler(self.event_handlers[0])
        mock.assert_called_with(self.event_handlers[0])

    @patch.object(EventResourceApi, 'update_event_handler')
    def test_updateEventHandler(self, mock):
        self.event_client.updateEventHandler(self.event_handlers[1])
        mock.assert_called_with(self.event_handlers[1])
        
    @patch.object(EventResourceApi, 'get_event_handlers_for_event')
    def test_getEventHandlers_activeOnly(self, mock):
        mock.return_value = [self.event_handlers[0]]
        event_handlers = self.event_client.getEventHandlers(EVENT_NAME)
        mock.assert_called_with(EVENT_NAME, active_only=True)
        self.assertListEqual(event_handlers, [self.event_handlers[0]])

    @patch.object(EventResourceApi, 'get_event_handlers_for_event')
    def test_getEventHandlers_all(self, mock):
        mock.return_value = self.event_handlers
        event_handlers = self.event_client.getEventHandlers(EVENT_NAME, False)
        mock.assert_called_with(EVENT_NAME, active_only=False)
        self.assertListEqual(event_handlers, self.event_handlers)
        
    @patch.object(EventResourceApi, 'remove_event_handler_status')
    def test_unregisterEventHandler(self, mock):
        self.event_client.unregisterEventHandler(EVENT_NAME)
        mock.assert_called_with(EVENT_NAME)
    
    @patch.object(EventResourceApi, 'put_queue_config')
    def test_putQueueConfig(self, mock):
        self.event_client.putQueueConfig(QUEUE_TYPE, QUEUE_NAME, {})
        mock.assert_called_with('{}', QUEUE_TYPE, QUEUE_NAME)
        
    @patch.object(EventResourceApi, 'get_queue_config')
    def test_getQueueConfig(self, mock):
        configs = {
            QUEUE_TYPE + ":" + QUEUE_NAME : {},
            QUEUE_TYPE + ":another_queue_name" : {},
        }
        mock.return_value = configs
        config_map = self.event_client.getQueueConfig(QUEUE_TYPE, QUEUE_NAME)
        mock.assert_called_with(QUEUE_TYPE, QUEUE_NAME)
        self.assertDictEqual(config_map, configs)
    
    @patch.object(EventResourceApi, 'delete_queue_config')
    def test_deleteQueueConfig(self, mock):
        self.event_client.deleteQueueConfig(QUEUE_TYPE, QUEUE_NAME)
        mock.assert_called_with(QUEUE_TYPE, QUEUE_NAME)