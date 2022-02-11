from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.health_check_resource_api import HealthCheckResourceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestHealthCheckResourceApi(unittest.TestCase):
    """HealthCheckResourceApi unit test stubs"""

    def setUp(self):
        self.api = HealthCheckResourceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_do_check(self):
        """Test case for do_check

        """
        pass


if __name__ == '__main__':
    unittest.main()
