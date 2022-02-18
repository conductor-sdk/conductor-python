from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.worker.sample.faulty_execution_worker import FaultyExecutionWorker
from conductor.client.worker.sample.simple_python_worker import SimplePythonWorker
from unittest.mock import patch
import logging
import unittest


class TestTaskRunner(unittest.TestCase):
    TASK_ID = 'TASK_ID'
    WORKFLOW_INSTANCE_ID = 'WORKFLOW_INSTANCE_ID'

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_initialization_with_invalid_configuration(self):
        expected_exception = Exception('Invalid configuration')
        with self.assertRaises(Exception) as context:
            TaskRunner(
                configuration=None,
                worker=SimplePythonWorker()
            )
        self.assertEqual(str(expected_exception), str(context.exception))

    def test_initialization_with_invalid_worker(self):
        expected_exception = Exception('Invalid worker')
        with self.assertRaises(Exception) as context:
            TaskRunner(
                configuration=Configuration(),
                worker=None
            )
        self.assertEqual(str(expected_exception), str(context.exception))

    def test_poll_task(self):
        expected_task = self.__get_valid_task()
        with patch.object(
            TaskResourceApi,
            'poll',
            return_value=self.__get_valid_task()
        ):
            task_runner = self.__get_valid_task_runner()
            task = task_runner._TaskRunner__poll_task()
            self.assertEqual(task, expected_task)

    def test_poll_task_with_faulty_task_api(self):
        expected_task = None
        with patch.object(
            TaskResourceApi,
            'poll',
            side_effect=Exception()
        ):
            task_runner = self.__get_valid_task_runner()
            task = task_runner._TaskRunner__poll_task()
            self.assertEqual(task, expected_task)

    def test_execute_task_with_invalid_task(self):
        task_runner = self.__get_valid_task_runner()
        task_result = task_runner._TaskRunner__execute_task(None)
        self.assertEqual(task_result, None)

    def test_execute_task_with_faulty_execution_worker(self):
        worker = FaultyExecutionWorker()
        expected_task_result = TaskResult(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID,
            worker_id=worker.get_task_definition_name(),
            status='FAILED',
            reason_for_incompletion='faulty execution'
        )
        task_runner = TaskRunner(
            configuration=Configuration(),
            worker=worker
        )
        task = self.__get_valid_task()
        task_result = task_runner._TaskRunner__execute_task(task)
        self.assertEqual(task_result, expected_task_result)

    def test_execute_task(self):
        worker = SimplePythonWorker()
        expected_task_result = TaskResult(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID,
            worker_id=worker.get_task_definition_name(),
            status='COMPLETED',
            output_data={
                'key': 'value'
            }
        )
        task_runner = TaskRunner(
            configuration=Configuration(),
            worker=worker
        )
        task = self.__get_valid_task()
        task_result = task_runner._TaskRunner__execute_task(task)
        self.assertEqual(task_result, expected_task_result)

    def test_wait_for_polling_interval_with_faulty_worker(self):
        expected_exception = Exception(
            "Failed to get polling interval"
        )
        with patch.object(
            SimplePythonWorker,
            'get_polling_interval_in_seconds',
            side_effect=expected_exception
        ):
            task_runner = self.__get_valid_task_runner()
            with self.assertRaises(Exception) as context:
                task_runner._TaskRunner__wait_for_polling_interval()
            self.assertEqual(str(expected_exception), str(context.exception))

    def test_wait_for_polling_interval(self):
        task_runner = self.__get_valid_task_runner()
        # TODO: add stopwatch to validate if the thread slept at least for `polling_interval` seconds
        task_runner._TaskRunner__wait_for_polling_interval()

    def __get_valid_task_runner(self):
        return TaskRunner(
            configuration=Configuration(),
            worker=SimplePythonWorker()
        )

    def __get_valid_task(self):
        return Task(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID
        )
