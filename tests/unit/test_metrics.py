from conductor.client.configuration.settings.metrics_settings import MetricsSettings
import logging
import unittest


class TestMetricsCollection(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_default_initialization(self):
        metrics_settings = MetricsSettings()
        self.assertIsNotNone(metrics_settings)
