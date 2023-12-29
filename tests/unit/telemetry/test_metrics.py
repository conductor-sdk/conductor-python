import logging
import unittest

from conductor.client.configuration.settings.metrics_settings import MetricsSettings


class TestMetricsCollection(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_default_initialization(self):
        metrics_settings = MetricsSettings()
        self.assertEqual(metrics_settings.file_name, 'metrics.log')
        self.assertEqual(metrics_settings.update_interval, 0.1)

    def test_default_initialization_with_parameters(self):
        expected_directory = '/a/b'
        expected_file_name = 'some_name.txt'
        expected_update_interval = 0.5
        metrics_settings = MetricsSettings(
            directory=expected_directory,
            file_name=expected_file_name,
            update_interval=expected_update_interval,
        )
        self.assertEqual(
            metrics_settings.file_name,
            expected_file_name
        )
        self.assertEqual(
            metrics_settings.update_interval,
            expected_update_interval
        )
