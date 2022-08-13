import base64
import unittest

from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient


class TestConfiguration(unittest.TestCase):
    def test_initialization_default(self):
        configuration = Configuration()
        self.assertEqual(
            configuration.host,
            'http://localhost:8080/api/'
        )

    def test_initialization_with_base_url(self):
        configuration = Configuration(
            base_url='https://play.orkes.io'
        )
        self.assertEqual(
            configuration.host,
            'https://play.orkes.io/api/'
        )

    def test_initialization_with_server_api_url(self):
        configuration = Configuration(
            server_api_url='https://play.orkes.io/api/'
        )
        self.assertEqual(
            configuration.host,
            'https://play.orkes.io/api/'
        )

    def test_initialization_with_basic_auth_server_api_url(self):
        configuration = Configuration(
            server_api_url="https://user:password@play.orkes.io/api/"
        )
        basic_auth = "user:password"
        self.assertEqual(configuration.host, f"https://{basic_auth}@play.orkes.io/api/")
        token = "Basic " + base64.b64encode(bytes(basic_auth, "utf-8")).decode("utf-8")
        api_client = ApiClient(configuration)
        self.assertEqual(
            api_client.default_headers,
            {"Accept-Encoding": "gzip", "authorization": token},
        )