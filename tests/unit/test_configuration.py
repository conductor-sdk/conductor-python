from conductor.client.configuration.configuration import Configuration
import unittest


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

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
