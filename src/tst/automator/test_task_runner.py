from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.sample.faulty_execution_worker import FaultyExecutionWorker
from conductor.client.worker.sample.simple_python_worker import SimplePythonWorker
from unittest.mock import patch
import logging
import time
import unittest


class TestTaskRunner(unittest.TestCase):
    TASK_ID = 'VALID_TASK_ID'
    WORKFLOW_INSTANCE_ID = 'VALID_WORKFLOW_INSTANCE_ID'
    UPDATE_TASK_RESPONSE = 'VALID_UPDATE_TASK_RESPONSE'

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_initialization_with_invalid_configuration(self):
        expected_exception = Exception('Invalid configuration')
        with self.assertRaises(Exception) as context:
            TaskRunner(
                configuration=None,
                worker=self.__get_valid_worker()
            )
            self.assertEqual(expected_exception, context.exception)

    def test_initialization_with_invalid_worker(self):
        expected_exception = Exception('Invalid worker')
        with self.assertRaises(Exception) as context:
            TaskRunner(
                configuration=Configuration(),
                worker=None
            )
            self.assertEqual(expected_exception, context.exception)

    def test_run_once(self):
        expected_time = self.__get_valid_worker().get_polling_interval_in_seconds()
        with patch.object(
            TaskResourceApi,
            'poll',
            return_value=self.__get_valid_task()
        ):
            with patch.object(
                TaskResourceApi,
                'update_task',
                return_value=self.UPDATE_TASK_RESPONSE
            ):
                task_runner = self.__get_valid_task_runner()
                start_time = time.time()
                task_runner.run_once()
                finish_time = time.time()
                spent_time = finish_time - start_time
                self.assertGreater(spent_time, expected_time)

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
        worker = FaultyExecutionWorker('task')
        expected_task_result = TaskResult(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID,
            worker_id=worker.get_identity(),
            status=TaskResultStatus.FAILED,
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
        expected_task_result = self.__get_valid_task_result()
        worker = self.__get_valid_worker()
        task_runner = TaskRunner(
            configuration=Configuration(),
            worker=worker
        )
        task = self.__get_valid_task()
        task_result = task_runner._TaskRunner__execute_task(task)
        self.assertEqual(task_result, expected_task_result)

    def test_update_task_with_invalid_task_result(self):
        expected_response = None
        task_runner = self.__get_valid_task_runner()
        response = task_runner._TaskRunner__update_task(None)
        self.assertEqual(response, expected_response)

    def test_update_task_with_faulty_task_api(self):
        expected_response = None
        with patch.object(
            TaskResourceApi,
            'update_task',
            side_effect=Exception()
        ):
            task_runner = self.__get_valid_task_runner()
            task_result = self.__get_valid_task_result()
            response = task_runner._TaskRunner__update_task(task_result)
            self.assertEqual(response, expected_response)

    def test_update_task(self):
        expected_response = self.UPDATE_TASK_RESPONSE
        with patch.object(
            TaskResourceApi,
            'update_task',
            return_value=self.UPDATE_TASK_RESPONSE
        ):
            task_runner = self.__get_valid_task_runner()
            task_result = self.__get_valid_task_result()
            response = task_runner._TaskRunner__update_task(task_result)
            self.assertEqual(response, expected_response)

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
                self.assertEqual(expected_exception, context.exception)

    def test_wait_for_polling_interval(self):
        expected_time = self.__get_valid_worker().get_polling_interval_in_seconds()
        task_runner = self.__get_valid_task_runner()
        start_time = time.time()
        task_runner._TaskRunner__wait_for_polling_interval()
        finish_time = time.time()
        spent_time = finish_time - start_time
        self.assertGreater(spent_time, expected_time)

    def __get_valid_task_runner(self):
        return TaskRunner(
            configuration=Configuration(),
            worker=self.__get_valid_worker()
        )

    def __get_valid_task(self):
        return Task(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID
        )

    def __get_valid_task_result(self):
        return TaskResult(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID,
            worker_id=self.__get_valid_worker().get_identity(),
            status=TaskResultStatus.COMPLETED,
            output_data={
                'key': 'value'
            }
        )

    def __get_valid_worker(self):
        return SimplePythonWorker('task')
