from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from tests.resources.worker.python.python_worker import SimplePythonWorker
import unittest


class TestTaskHandler(unittest.TestCase):
    def test_initialization_with_invalid_workers(self):
        expected_exception = Exception('Invalid worker list')
        with self.assertRaises(Exception) as context:
            TaskHandler(
                configuration=Configuration(),
                workers=SimplePythonWorker()
            )
            self.assertEqual(expected_exception, context.exception)

    def test_start_processes(self):
        task_handler = TaskHandler(
            configuration=Configuration(),
            workers=[
                SimplePythonWorker('task')
            ]
        )
        self.assertIsNotNone(task_handler)
        task_handler.start_processes()
