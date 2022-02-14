from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.event_resource_api import EventResourceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestEventResourceApi(unittest.TestCase):
    """EventResourceApi unit test stubs"""

    def setUp(self):
        self.api = EventResourceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_event_handler(self):
        """Test case for add_event_handler

        Add a new event handler.  # noqa: E501
        """
        pass

    def test_get_event_handlers(self):
        """Test case for get_event_handlers

        Get all the event handlers  # noqa: E501
        """
        pass

    def test_get_event_handlers_for_event(self):
        """Test case for get_event_handlers_for_event

        Get event handlers for a given event  # noqa: E501
        """
        pass

    def test_remove_event_handler_status(self):
        """Test case for remove_event_handler_status

        Remove an event handler  # noqa: E501
        """
        pass

    def test_update_event_handler(self):
        """Test case for update_event_handler

        Update an existing event handler.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
