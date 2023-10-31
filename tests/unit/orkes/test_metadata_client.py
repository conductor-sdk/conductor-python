import logging
import unittest

from unittest.mock import Mock, patch, MagicMock
from conductor.client.http.rest import ApiException, RESTResponse
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.orkes.api.tags_api import TagsApi
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.tag_string import TagString
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.models.ratelimit_tag import RateLimitTag
from conductor.client.http.models.task_def import TaskDef

WORKFLOW_NAME = 'ut_wf'
TASK_NAME = 'ut_task'
ERROR_BODY= '{"message":"No such workflow found by name"}'

class TestOrkesMetadataClient(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.metadata_client = OrkesMetadataClient(configuration)
        
    def setUp(self):
        self.workflowDef = WorkflowDef(name=WORKFLOW_NAME, version=1)
        self.taskDef = TaskDef(TASK_NAME)
        self.wfTagObj = MetadataTag("test", "val")
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "metadataResourceApi is not of type MetadataResourceApi"
        self.assertIsInstance(self.metadata_client.metadataResourceApi, MetadataResourceApi, message)

    @patch.object(MetadataResourceApi, 'create')
    def test_registerWorkflowDef(self, mock):
        self.metadata_client.registerWorkflowDef(self.workflowDef)
        self.assertTrue(mock.called)
        mock.assert_called_with(self.workflowDef, overwrite=True)

    @patch.object(MetadataResourceApi, 'create')
    def test_registerWorkflowDef_without_overwrite(self, mock):
        self.metadata_client.registerWorkflowDef(self.workflowDef, False)
        self.assertTrue(mock.called)
        mock.assert_called_with(self.workflowDef, overwrite=False)

    @patch.object(MetadataResourceApi, 'update1')
    def test_updateWorkflowDef(self, mock):
        self.metadata_client.updateWorkflowDef(self.workflowDef)
        self.assertTrue(mock.called)
        mock.assert_called_with([self.workflowDef], overwrite=True)

    @patch.object(MetadataResourceApi, 'update1')
    def test_updateWorkflowDef_without_overwrite(self, mock):
        self.metadata_client.updateWorkflowDef(self.workflowDef, False)
        self.assertTrue(mock.called)
        mock.assert_called_with([self.workflowDef], overwrite=False)

    @patch.object(MetadataResourceApi, 'unregister_workflow_def')
    def test_unregisterWorkflowDef(self, mock):
        self.metadata_client.unregisterWorkflowDef(WORKFLOW_NAME, 1)
        self.assertTrue(mock.called)
        mock.assert_called_with(WORKFLOW_NAME, 1)
        
    @patch.object(MetadataResourceApi, 'get')
    def test_getWorkflowDef_without_version(self, mock):
        mock.return_value = self.workflowDef
        wf, _ = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        self.assertEqual(wf, self.workflowDef)
        self.assertTrue(mock.called)
        mock.assert_called_with(WORKFLOW_NAME)
    
    @patch.object(MetadataResourceApi, 'get')
    def test_getWorkflowDef_with_version(self, mock):
        mock.return_value = self.workflowDef
        wf, _ = self.metadata_client.getWorkflowDef(WORKFLOW_NAME, 1)
        self.assertEqual(wf, self.workflowDef)
        mock.assert_called_with(WORKFLOW_NAME, version=1)
    
    @patch.object(MetadataResourceApi, 'get')
    def test_getWorkflowDef_non_existent(self, mock):
        mock.side_effect = MagicMock(side_effect=ApiException(status=404, reason=ERROR_BODY))
        wf, error = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        self.assertIsNone(wf, "workflow is not None")
        self.assertEqual(error, "Error in fetching workflow: " + ERROR_BODY)
        
    @patch.object(MetadataResourceApi, 'get_all_workflows')
    def test_getAllWorkflowDefs(self, mock):
        workflowDef2 = WorkflowDef(name='ut_wf_2', version=1)
        mock.return_value = [self.workflowDef, workflowDef2]
        wfs = self.metadata_client.getAllWorkflowDefs()
        self.assertEqual(len(wfs), 2)
    
    @patch.object(MetadataResourceApi, 'register_task_def')
    def test_registerTaskDef(self, mock):
        self.metadata_client.registerTaskDef(self.taskDef)
        self.assertTrue(mock.called)
        mock.assert_called_with([self.taskDef])
    
    @patch.object(MetadataResourceApi, 'update_task_def')
    def test_updateTaskDef(self, mock):
        self.metadata_client.updateTaskDef(self.taskDef)
        self.assertTrue(mock.called)
        mock.assert_called_with(self.taskDef)
    
    @patch.object(MetadataResourceApi, 'unregister_task_def')
    def test_unregisterTaskDef(self, mock):
        self.metadata_client.unregisterTaskDef(TASK_NAME)
        self.assertTrue(mock.called)
        mock.assert_called_with(TASK_NAME)

    @patch.object(MetadataResourceApi, 'get_task_def')
    def test_getTaskDef(self, mock):
        mock.return_value = self.taskDef
        taskDefinition = self.metadata_client.getTaskDef(TASK_NAME)
        self.assertEqual(taskDefinition, self.taskDef)
        mock.assert_called_with(TASK_NAME)

    @patch.object(MetadataResourceApi, 'get_task_defs')
    def test_getAllTaskDefs(self, mock):
        taskDef2 = TaskDef("ut_task2")
        mock.return_value = [self.taskDef, taskDef2]
        tasks = self.metadata_client.getAllTaskDefs()
        self.assertEqual(len(tasks), 2)

    @patch.object(TagsApi, 'add_workflow_tag')
    def test_addWorkflowTag(self, mock):
        self.metadata_client.addWorkflowTag(self.wfTagObj, WORKFLOW_NAME)
        mock.assert_called_with(self.wfTagObj, WORKFLOW_NAME)

    @patch.object(TagsApi, 'delete_workflow_tag')
    def test_deleteWorkflowTag(self, mock):
        wfTagOStr = TagString("test", "METADATA", "val")
        self.metadata_client.deleteWorkflowTag(self.wfTagObj, WORKFLOW_NAME)
        mock.assert_called_with(wfTagOStr, WORKFLOW_NAME)

    @patch.object(TagsApi, 'set_workflow_tags')
    def test_setWorkflowTags(self, mock):
        wfTagObj2 = MetadataTag("test2", "val2")
        wfTagObjs = [self.wfTagObj, wfTagObj2]
        self.metadata_client.setWorkflowTags(wfTagObjs, WORKFLOW_NAME)
        mock.assert_called_with(wfTagObjs, WORKFLOW_NAME)

    @patch.object(TagsApi, 'get_workflow_tags')
    def test_getWorkflowTags(self, mock):
        wfTagObj2 = MetadataTag("test2", "val2")
        mock.return_value = [self.wfTagObj, wfTagObj2]
        tags = self.metadata_client.getWorkflowTags(WORKFLOW_NAME)
        mock.assert_called_with(WORKFLOW_NAME)
        self.assertEqual(len(tags), 2)

    @patch.object(TagsApi, 'add_task_tag')
    def test_addTaskTag(self, mock):
        taskTag = MetadataTag("tag1", "val1")
        self.metadata_client.addTaskTag(taskTag, TASK_NAME)
        mock.assert_called_with(taskTag, TASK_NAME)

    @patch.object(TagsApi, 'delete_task_tag')
    def test_deleteTaskTag(self, mock):
        taskTag = MetadataTag("tag1", "val1")
        taskTagStr = TagString("tag1", "METADATA", "val1")
        self.metadata_client.deleteTaskTag(taskTag, TASK_NAME)
        mock.assert_called_with(taskTagStr, TASK_NAME)

    @patch.object(TagsApi, 'set_task_tags')
    def test_setTaskTags(self, mock):
        taskTag1 = MetadataTag("tag1", "val1")
        taskTag2 = MetadataTag("tag2", "val2")
        taskTagObjs = [taskTag1, taskTag2]
        self.metadata_client.setTaskTags(taskTagObjs, TASK_NAME)
        mock.assert_called_with(taskTagObjs, TASK_NAME)

    @patch.object(TagsApi, 'get_task_tags')
    def test_getTaskTags(self, mock):
        taskTag1 = MetadataTag("tag1", "val1")
        taskTag2 = MetadataTag("tag2", "val2")
        mock.return_value = [taskTag1, taskTag2]
        tags = self.metadata_client.getTaskTags(TASK_NAME)
        mock.assert_called_with(TASK_NAME)
        self.assertEqual(len(tags), 2)

    @patch.object(TagsApi, 'get_workflow_tags')
    @patch.object(TagsApi, 'add_workflow_tag')
    def test_setWorkflowRateLimit(self, mockSet, mockRemove):
        mockRemove.return_value = []
        rateLimitTag = RateLimitTag(WORKFLOW_NAME, 5)
        self.metadata_client.setWorkflowRateLimit(5, WORKFLOW_NAME)
        mockRemove.assert_called_with(WORKFLOW_NAME)
        mockSet.assert_called_with(rateLimitTag, WORKFLOW_NAME)

    @patch.object(TagsApi, 'get_workflow_tags')
    def test_getWorkflowRateLimit(self, mock):
        metadataTag = MetadataTag("test", "val")
        rateLimitTag = RateLimitTag(WORKFLOW_NAME, 5)
        mock.return_value = [metadataTag, rateLimitTag]
        rateLimit = self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME)
        self.assertEqual(rateLimit, 5)

    @patch.object(TagsApi, 'get_workflow_tags')
    def test_getWorkflowRateLimit_not_set(self, mock):
        mock.return_value = []
        rateLimit = self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME)
        mock.assert_called_with(WORKFLOW_NAME)
        self.assertIsNone(rateLimit)

    @patch.object(OrkesMetadataClient, 'getWorkflowRateLimit')
    @patch.object(TagsApi, 'delete_workflow_tag')
    def test_removeWorkflowRateLimit(self, patchedTagsApi, patchedMetadataClient):
        patchedMetadataClient.return_value = 5
        self.metadata_client.removeWorkflowRateLimit(WORKFLOW_NAME)
        rateLimitTag = RateLimitTag(WORKFLOW_NAME, 5)
        patchedTagsApi.assert_called_with(rateLimitTag, WORKFLOW_NAME)

