import logging
import unittest
import json

from unittest.mock import Mock, patch, MagicMock

from conductor.client.orkes.orkes_task_client import OrkesTaskClient
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.task import Task
from conductor.client.http.rest import ApiException
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.http.models.task_exec_log import TaskExecLog
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.http.models.workflow import Workflow
from conductor.client.exceptions.api_error import APIError

TASK_NAME = 'ut_task'
TASK_ID = 'task_id_1'
TASK_NAME_2 = 'ut_task_2'
WORKER_ID = "ut_worker_id"
DOMAIN = "test_domain"

class TestOrkesTaskClient(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.task_client = OrkesTaskClient(configuration)
        
    def setUp(self):
        self.tasks = [
            Task(task_type=TaskType.SIMPLE, task_def_name=TASK_NAME, reference_task_name="simple_task_ref_1", task_id=TASK_ID),
            Task(task_type=TaskType.SIMPLE, task_def_name=TASK_NAME, reference_task_name="simple_task_ref_2", task_id="task_id_2"),
            Task(task_type=TaskType.SIMPLE, task_def_name=TASK_NAME, reference_task_name="simple_task_ref_3", task_id="task_id_3"),
        ]
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "taskResourceApi is not of type TaskResourceApi"
        self.assertIsInstance(self.task_client.taskResourceApi, TaskResourceApi, message)

    @patch.object(TaskResourceApi, 'poll')
    def test_pollTask(self, mock):
        mock.return_value = self.tasks[0]
        polledTask = self.task_client.pollTask(TASK_NAME)
        mock.assert_called_with(TASK_NAME)
        self.assertEqual(polledTask, self.tasks[0])

    @patch.object(TaskResourceApi, 'poll')
    def test_pollTask_with_worker_and_domain(self, mock):
        mock.return_value = self.tasks[0]
        polledTask = self.task_client.pollTask(TASK_NAME, WORKER_ID, DOMAIN)
        mock.assert_called_with(TASK_NAME, workerid=WORKER_ID, domain=DOMAIN)
        self.assertEqual(polledTask, self.tasks[0])
    
    @patch.object(TaskResourceApi, 'poll')
    def test_pollTask_no_tasks(self, mock):
        mock.return_value = None
        polledTask = self.task_client.pollTask(TASK_NAME)
        mock.assert_called_with(TASK_NAME)
        self.assertIsNone(polledTask)
    
    @patch.object(TaskResourceApi, 'batch_poll')
    def test_batchPollTasks(self, mock):
        mock.return_value = self.tasks
        polledTasks = self.task_client.batchPollTasks(TASK_NAME, WORKER_ID, 3, 200)
        mock.assert_called_with(TASK_NAME, workerid=WORKER_ID, count=3, timeout=200)
        self.assertEqual(len(polledTasks), len(self.tasks))
    
    @patch.object(TaskResourceApi, 'batch_poll')
    def test_batchPollTasks_in_domain(self, mock):
        mock.return_value = self.tasks
        polledTasks = self.task_client.batchPollTasks(TASK_NAME, WORKER_ID, 3, 200, DOMAIN)
        mock.assert_called_with(TASK_NAME, workerid=WORKER_ID, domain=DOMAIN, count=3, timeout=200)
        self.assertEqual(len(polledTasks), len(self.tasks))
    
    @patch.object(TaskResourceApi, 'get_task')
    def test_getTask(self, mock):
        mock.return_value = self.tasks[0]
        task = self.task_client.getTask(TASK_ID)
        mock.assert_called_with(TASK_ID)
        self.assertEqual(task.task_id, TASK_ID)

    @patch.object(TaskResourceApi, 'get_task')
    def test_getTask_non_existent(self, mock):
        error_body = { 'status': 404, 'message': 'Task not found' }
        mock.side_effect = MagicMock(side_effect=ApiException(status=404, body=json.dumps(error_body)))
        with self.assertRaises(APIError):
            self.task_client.getTask(TASK_ID)
            mock.assert_called_with(TASK_ID)
        
    @patch.object(TaskResourceApi, 'update_task')
    def test_updateTask(self, mock):
        taskResultStatus = TaskResult(task_id=TASK_ID, status=TaskResultStatus.COMPLETED)
        self.task_client.updateTask(taskResultStatus)
        mock.assert_called_with(taskResultStatus)
    
    @patch.object(TaskResourceApi, 'update_task1')
    def test_updateTaskByRefName(self, mock):
        status = TaskResultStatus.COMPLETED
        output = { "a":  56 }
        self.task_client.updateTaskByRefName(
            "wf_id", "test_task_ref_name", status, output
        )
        mock.assert_called_with({"result": output}, "wf_id", "test_task_ref_name", status)
    
    @patch.object(TaskResourceApi, 'update_task1')
    def test_updateTaskByRefName_with_workerId(self, mock):
        status = TaskResultStatus.COMPLETED
        output = { "a":  56 }
        self.task_client.updateTaskByRefName(
            "wf_id", "test_task_ref_name", status, output, "worker_id"
        )
        mock.assert_called_with({"result": output}, "wf_id", "test_task_ref_name", status, workerid="worker_id")

    @patch.object(TaskResourceApi, 'update_task_sync')
    def test_updateTaskSync(self, mock):
        workflowId = "test_wf_id"
        workflow = Workflow(workflow_id=workflowId)
        mock.return_value = workflow
        status = TaskResultStatus.COMPLETED
        output = { "a":  56 }
        returnedWorkflow = self.task_client.updateTaskSync(
            workflowId, "test_task_ref_name", status, output
        )
        mock.assert_called_with({"result": output}, workflowId, "test_task_ref_name", status)
        self.assertEqual(returnedWorkflow, workflow)

    @patch.object(TaskResourceApi, 'update_task_sync')
    def test_updateTaskSync_with_workerId(self, mock):
        workflowId = "test_wf_id"
        workflow = Workflow(workflow_id=workflowId)
        mock.return_value = workflow
        status = TaskResultStatus.COMPLETED
        output = { "a":  56 }
        returnedWorkflow = self.task_client.updateTaskSync(
            workflowId, "test_task_ref_name", status, output, "worker_id"
        )
        mock.assert_called_with({"result": output}, workflowId, "test_task_ref_name", status, workerid="worker_id")
        self.assertEqual(returnedWorkflow, workflow)

    @patch.object(TaskResourceApi, 'size')
    def test_getQueueSizeForTask(self, mock):
        mock.return_value = { TASK_NAME: 4 }
        size = self.task_client.getQueueSizeForTask(TASK_NAME)
        mock.assert_called_with(task_type=[TASK_NAME])
        self.assertEqual(size, 4)
    
    @patch.object(TaskResourceApi, 'size')
    def test_getQueueSizeForTask_empty(self, mock):
        mock.return_value = {}
        size = self.task_client.getQueueSizeForTask(TASK_NAME)
        mock.assert_called_with(task_type=[TASK_NAME])
        self.assertEqual(size, 0)

    @patch.object(TaskResourceApi, 'log')
    def test_addTaskLog(self, mock):
        logMessage = "Test log"
        self.task_client.addTaskLog(TASK_ID, logMessage)
        mock.assert_called_with(logMessage, TASK_ID)

    @patch.object(TaskResourceApi, 'get_task_logs')
    def test_getTaskLogs(self, mock):
        taskExecLog1 = TaskExecLog("Test log 1", TASK_ID)
        taskExecLog2 = TaskExecLog("Test log 2", TASK_ID)
        mock.return_value = [taskExecLog1, taskExecLog2]
        logs = self.task_client.getTaskLogs(TASK_ID)
        mock.assert_called_with(TASK_ID)
        self.assertEqual(len(logs), 2)
