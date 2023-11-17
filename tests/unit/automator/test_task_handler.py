from conductor.client.automator.task_handler import TaskHandler
from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from tests.unit.resources.workers import ClassWorker
from unittest.mock import Mock, MagicMock
from unittest.mock import patch
from configparser import ConfigParser
import multiprocessing
import unittest
import tempfile


class PickableMock(Mock):
    def __reduce__(self):
        return (Mock, ())


class TestTaskHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.application_properties = tempfile.NamedTemporaryFile(delete=False)
        return super().setUp()

    def tearDown(self) -> None:
        self.application_properties.close()
        return super().tearDown()

    def test_initialization_with_invalid_workers(self):
        expected_exception = Exception('Invalid worker list')
        with self.assertRaises(Exception) as context:
            TaskHandler(
                configuration=Configuration(),
                workers=ClassWorker()
            )
            self.assertEqual(expected_exception, context.exception)

    def test_start_processes(self):
        with patch.object(TaskRunner, 'run', PickableMock(return_value=None)):
            with _get_valid_task_handler() as task_handler:
                task_handler.start_processes()
                self.assertEqual(len(task_handler.task_runner_processes), 1)
                for process in task_handler.task_runner_processes:
                    self.assertTrue(
                        isinstance(process, multiprocessing.Process)
                    )

    @patch("multiprocessing.Process.kill", Mock(return_value=None))
    def test_initialize_with_no_worker_config(self):
        with _get_valid_task_handler() as task_handler:
            worker_config = task_handler.worker_config
            self.assertIsInstance(worker_config, ConfigParser)
            self.assertEqual(len(worker_config.sections()), 0)

    @patch("multiprocessing.Process.kill", Mock(return_value=None))
    def test_initialize_with_worker_config(self):
        with tempfile.NamedTemporaryFile(mode='w+') as tf:
            configParser = ConfigParser()
            configParser.add_section('task')
            configParser.set('task', 'domain', 'test')
            configParser.set('task', 'pollingInterval', '2.0')
            configParser.add_section('task2')
            configParser.set('task2', 'domain', 'test2')
            configParser.set('task2', 'pollingInterval', '3.0')
            configParser.write(tf)
            tf.seek(0)
            
            def get_config_file_path_mock():
                return tf.name

            with patch('conductor.client.automator.task_handler.__get_config_file_path', get_config_file_path_mock):
                with _get_valid_task_handler() as task_handler:
                    config = task_handler.worker_config
                    self.assertIsInstance(config, ConfigParser)
                    self.assertEqual(len(config.sections()), 2)
                    self.assertEqual(config.get('task', 'domain'), "test")
                    self.assertEqual(config.get('task', 'pollingInterval'), "2.0")
                    self.assertEqual(config.get('task2', 'domain'), "test2")
                    self.assertEqual(config.get('task2', 'pollingInterval'), "3.0")

def _get_valid_task_handler():
    return TaskHandler(
        configuration=Configuration(),
        workers=[
            ClassWorker('task')
        ]
    )
