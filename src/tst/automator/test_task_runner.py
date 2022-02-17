import logging
from conductor.client.automator.task_runner import TaskRunner
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.worker.sample.faulty_execution_worker import FaultyExecutionWorker
from conductor.client.worker.sample.simple_python_worker import SimplePythonWorker
from unittest.mock import MagicMock
import unittest


class TestTaskRunner(unittest.TestCase):
    TASK_ID = 'TASK_ID'
    WORKFLOW_INSTANCE_ID = 'WORKFLOW_INSTANCE_ID'

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_execute_task_with_invalid_task(self):
        task_runner = TaskRunner(
            configuration=MagicMock(),
            worker=MagicMock()
        )
        task_result = task_runner._TaskRunner__execute_task(MagicMock())
        self.assertEqual(task_result, None)

    def test_execute_task_with_faulty_execution_worker(self):
        worker = FaultyExecutionWorker()
        task_runner = TaskRunner(
            configuration=MagicMock(),
            worker=worker
        )
        task = Task(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID
        )
        task_result = task_runner._TaskRunner__execute_task(task)
        expected_task_result = TaskResult(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID,
            worker_id=worker.get_task_definition_name(),
            status='FAILED',
            reason_for_incompletion='faulty execution'
        )
        self.assertEqual(task_result, expected_task_result)

    def test_execute_task(self):
        worker = SimplePythonWorker()
        task_runner = TaskRunner(
            configuration=MagicMock(),
            worker=worker
        )
        task = Task(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID
        )
        task_result = task_runner._TaskRunner__execute_task(task)
        expected_task_result = TaskResult(
            task_id=self.TASK_ID,
            workflow_instance_id=self.WORKFLOW_INSTANCE_ID,
            worker_id=worker.get_task_definition_name(),
            status='COMPLETED',
            output_data={
                'key': 'value'
            }
        )
        self.assertEqual(task_result, expected_task_result)
