from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.metadata_resource_api import MetadataResourceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestMetadataResourceApi(unittest.TestCase):
    """MetadataResourceApi unit test stubs"""

    def setUp(self):
        self.api = MetadataResourceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create(self):
        """Test case for create

        Create a new workflow definition  # noqa: E501
        """
        pass

    def test_get(self):
        """Test case for get

        Retrieves workflow definition along with blueprint  # noqa: E501
        """
        pass

    def test_get_all(self):
        """Test case for get_all

        Retrieves all workflow definition along with blueprint  # noqa: E501
        """
        pass

    def test_get_task_def(self):
        """Test case for get_task_def

        Gets the task definition  # noqa: E501
        """
        pass

    def test_get_task_defs(self):
        """Test case for get_task_defs

        Gets all task definition  # noqa: E501
        """
        pass

    def test_register_task_def(self):
        """Test case for register_task_def

        Update an existing task  # noqa: E501
        """
        pass

    def test_register_task_def1(self):
        """Test case for register_task_def1

        Create new task definition(s)  # noqa: E501
        """
        pass

    def test_unregister_task_def(self):
        """Test case for unregister_task_def

        Remove a task definition  # noqa: E501
        """
        pass

    def test_unregister_workflow_def(self):
        """Test case for unregister_workflow_def

        Removes workflow definition. It does not remove workflows associated with the definition.  # noqa: E501
        """
        pass

    def test_update(self):
        """Test case for update

        Create or update workflow definition  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
