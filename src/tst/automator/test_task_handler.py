import unittest
from conductor.client.automator.task_handler import TaskHandler

from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.sample.simple_python_worker import SimplePythonWorker


class TestTaskHandler(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_initialization_with_invalid_worker(self):
        expected_exception = Exception('Invalid worker list')
        with self.assertRaises(Exception) as context:
            TaskHandler(
                configuration=Configuration(),
                workers=SimplePythonWorker()
            )
            self.assertEqual(expected_exception, context.exception)
