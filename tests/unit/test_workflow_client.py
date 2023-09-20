import logging
import unittest

from unittest.mock import Mock, patch, MagicMock
from conductor.client.http.rest import ApiException, RESTResponse
from conductor.client.orkes.workflow_client import WorkflowClient
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models.rerun_workflow_request import RerunWorkflowRequest
from conductor.client.http.models.workflow import Workflow
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.tag_string import TagString
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.models.ratelimit_tag import RateLimitTag
from conductor.client.http.models.task_def import TaskDef

WORKFLOW_NAME = 'ut_wf'
WORKFLOW_UUID = 'ut_wf_uuid'
TASK_NAME = 'ut_task'
CORRELATION_ID= 'correlation_id'
ERROR_BODY= '{"message":"No such workflow found by name"}'

class TestWorkflowClient(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.workflow_client = WorkflowClient(configuration)
        
    def setUp(self):
        self.input = {"a": "test"}
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "workflowResourceApi is not of type WorkflowResourceApi"
        self.assertIsInstance(self.workflow_client.workflowResourceApi, WorkflowResourceApi, message)

    @patch.object(WorkflowResourceApi, 'start_workflow1')
    def test_startWorkflow_with_name(self, mock):
        self.workflow_client.startWorkflow(WORKFLOW_NAME, self.input)
        mock.assert_called_with(self.input, WORKFLOW_NAME)
    
    @patch.object(WorkflowResourceApi, 'start_workflow1')
    def test_startWorkflow_with_version(self, mock):
        self.workflow_client.startWorkflow(WORKFLOW_NAME, self.input, version=1)
        mock.assert_called_with(self.input, WORKFLOW_NAME, version=1)

    @patch.object(WorkflowResourceApi, 'start_workflow1')
    def test_startWorkflow_with_correlation_id(self, mock):
        self.workflow_client.startWorkflow(WORKFLOW_NAME, self.input, correlationId=CORRELATION_ID)
        mock.assert_called_with(self.input, WORKFLOW_NAME, correlation_id=CORRELATION_ID)
    
    @patch.object(WorkflowResourceApi, 'start_workflow1')
    def test_startWorkflow_with_version_and_priority(self, mock):
        self.workflow_client.startWorkflow(WORKFLOW_NAME, self.input, version=1, priority=1)
        mock.assert_called_with(self.input, WORKFLOW_NAME, version=1, priority=1)
        
    @patch.object(WorkflowResourceApi, 'start_workflow')
    def test_startWorkflowFromWorkflowDef(self, mock):
        startWorkflowReq = StartWorkflowRequest()
        self.workflow_client.startWorkflowFromWorkflowDef(startWorkflowReq)
        mock.assert_called_with(startWorkflowReq)

    @patch.object(WorkflowResourceApi, 'pause_workflow1')
    def test_pauseWorkflow(self, mock):
        self.workflow_client.pauseWorkflow(WORKFLOW_UUID)
        mock.assert_called_with(WORKFLOW_UUID)
        
    @patch.object(WorkflowResourceApi, 'resume_workflow1')
    def test_resumeWorkflow(self, mock):
        self.workflow_client.resumeWorkflow(WORKFLOW_UUID)
        mock.assert_called_with(WORKFLOW_UUID)
    
    @patch.object(WorkflowResourceApi, 'restart1')
    def test_restartWorkflow(self, mock):
        self.workflow_client.restartWorkflow(WORKFLOW_UUID)
        mock.assert_called_with(WORKFLOW_UUID, use_latest_definitions=False)
    
    @patch.object(WorkflowResourceApi, 'restart1')
    def test_restartWorkflow_with_latest_wfDef(self, mock):
        self.workflow_client.restartWorkflow(WORKFLOW_UUID, True)
        mock.assert_called_with(WORKFLOW_UUID, use_latest_definitions=True)

    @patch.object(WorkflowResourceApi, 'rerun')
    def test_rerunWorkflow(self, mock):
        reRunReq = RerunWorkflowRequest()
        self.workflow_client.rerunWorkflow(WORKFLOW_UUID, reRunReq)
        mock.assert_called_with(reRunReq, WORKFLOW_UUID)
    
    @patch.object(WorkflowResourceApi, 'retry1')
    def test_retryWorkflow(self, mock):
        self.workflow_client.retryWorkflow(WORKFLOW_UUID)
        mock.assert_called_with(WORKFLOW_UUID, resume_subworkflow_tasks=False)

    @patch.object(WorkflowResourceApi, 'retry1')
    def test_retryWorkflow_with_resumeSubworkflowTasks(self, mock):
        self.workflow_client.retryWorkflow(WORKFLOW_UUID, True)
        mock.assert_called_with(WORKFLOW_UUID, resume_subworkflow_tasks=True)

    @patch.object(WorkflowResourceApi, 'terminate1')
    def test_terminateWorkflow(self, mock):
        self.workflow_client.terminateWorkflow(WORKFLOW_UUID)
        mock.assert_called_with(WORKFLOW_UUID)
        
    @patch.object(WorkflowResourceApi, 'terminate1')
    def test_terminateWorkflow_with_reason(self, mock):
        reason = "Unit test failed"
        self.workflow_client.terminateWorkflow(WORKFLOW_UUID, reason)
        mock.assert_called_with(WORKFLOW_UUID, reason=reason)
    
    @patch.object(WorkflowResourceApi, 'get_execution_status')
    def test_getWorkflow(self, mock):
        mock.return_value = Workflow(workflow_id=WORKFLOW_UUID)
        workflow, error = self.workflow_client.getWorkflow(WORKFLOW_UUID)
        mock.assert_called_with(WORKFLOW_UUID, include_tasks=True)
        self.assertEqual(workflow.workflow_id, WORKFLOW_UUID)
        self.assertIsNone(error)

    @patch.object(WorkflowResourceApi, 'get_execution_status')
    def test_getWorkflow_without_tasks(self, mock):
        mock.return_value = Workflow(workflow_id=WORKFLOW_UUID)
        workflow, error = self.workflow_client.getWorkflow(WORKFLOW_UUID, False)
        mock.assert_called_with(WORKFLOW_UUID, include_tasks=False)
        self.assertEqual(workflow.workflow_id, WORKFLOW_UUID)
        self.assertIsNone(error)

    @patch.object(WorkflowResourceApi, 'get_execution_status')
    def test_getWorkflow_non_existent(self, mock):
        mock.side_effect = MagicMock(side_effect=ApiException(status=404, reason="Not found"))
        workflow, error = self.workflow_client.getWorkflow(WORKFLOW_UUID, False)
        mock.assert_called_with(WORKFLOW_UUID, include_tasks=False)
        self.assertIsNone(workflow)
        self.assertEqual(error, "Not found")

    @patch.object(WorkflowResourceApi, 'delete')
    def test_deleteWorkflow(self, mock):
        workflow = self.workflow_client.deleteWorkflow(WORKFLOW_UUID)
        mock.assert_called_with(WORKFLOW_UUID, archive_workflow=True)

    @patch.object(WorkflowResourceApi, 'delete')
    def test_deleteWorkflow_without_archival(self, mock):
        workflow = self.workflow_client.deleteWorkflow(WORKFLOW_UUID, False)
        mock.assert_called_with(WORKFLOW_UUID, archive_workflow=False)