import logging
import unittest
import json

from unittest.mock import Mock, patch, MagicMock
from conductor.client.http.rest import ApiException
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.orkes.api.tags_api import TagsApi
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.tag_string import TagString
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.models.ratelimit_tag import RateLimitTag
from conductor.client.http.models.task_def import TaskDef
from conductor.client.exceptions.api_error import APIError

WORKFLOW_NAME = 'ut_wf'
TASK_NAME = 'ut_task'

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
        message = "metadata_resource_api is not of type MetadataResourceApi"
        self.assertIsInstance(self.metadata_client.metadata_resource_api, MetadataResourceApi, message)

    @patch.object(MetadataResourceApi, 'create')
    def test_registerWorkflowDef(self, mock):
        self.metadata_client.register_workflow_def(self.workflowDef)
        self.assertTrue(mock.called)
        mock.assert_called_with(self.workflowDef, overwrite=True)

    @patch.object(MetadataResourceApi, 'create')
    def test_registerWorkflowDef_without_overwrite(self, mock):
        self.metadata_client.register_workflow_def(self.workflowDef, False)
        self.assertTrue(mock.called)
        mock.assert_called_with(self.workflowDef, overwrite=False)

    @patch.object(MetadataResourceApi, 'update1')
    def test_updateWorkflowDef(self, mock):
        self.metadata_client.update_workflow_def(self.workflowDef)
        self.assertTrue(mock.called)
        mock.assert_called_with([self.workflowDef], overwrite=True)

    @patch.object(MetadataResourceApi, 'update1')
    def test_updateWorkflowDef_without_overwrite(self, mock):
        self.metadata_client.update_workflow_def(self.workflowDef, False)
        self.assertTrue(mock.called)
        mock.assert_called_with([self.workflowDef], overwrite=False)

    @patch.object(MetadataResourceApi, 'unregister_workflow_def')
    def test_unregisterWorkflowDef(self, mock):
        self.metadata_client.unregister_workflow_def(WORKFLOW_NAME, 1)
        self.assertTrue(mock.called)
        mock.assert_called_with(WORKFLOW_NAME, 1)
        
    @patch.object(MetadataResourceApi, 'get')
    def test_getWorkflowDef_without_version(self, mock):
        mock.return_value = self.workflowDef
        wf = self.metadata_client.get_workflow_def(WORKFLOW_NAME)
        self.assertEqual(wf, self.workflowDef)
        self.assertTrue(mock.called)
        mock.assert_called_with(WORKFLOW_NAME)
    
    @patch.object(MetadataResourceApi, 'get')
    def test_getWorkflowDef_with_version(self, mock):
        mock.return_value = self.workflowDef
        wf = self.metadata_client.get_workflow_def(WORKFLOW_NAME, 1)
        self.assertEqual(wf, self.workflowDef)
        mock.assert_called_with(WORKFLOW_NAME, version=1)
    
    @patch.object(MetadataResourceApi, 'get')
    def test_getWorkflowDef_non_existent(self, mock):
        message = 'No such workflow found by name:' + WORKFLOW_NAME + ', version: null'
        error_body = { 'status': 404, 'message': message }
        mock.side_effect = MagicMock(side_effect=ApiException(status=404, body=json.dumps(error_body)))
        with self.assertRaises(APIError):
            self.metadata_client.get_workflow_def(WORKFLOW_NAME)
        
    @patch.object(MetadataResourceApi, 'get_all_workflows')
    def test_getAllWorkflowDefs(self, mock):
        workflowDef2 = WorkflowDef(name='ut_wf_2', version=1)
        mock.return_value = [self.workflowDef, workflowDef2]
        wfs = self.metadata_client.get_all_workflow_defs()
        self.assertEqual(len(wfs), 2)
    
    @patch.object(MetadataResourceApi, 'register_task_def')
    def test_registerTaskDef(self, mock):
        self.metadata_client.register_task_def(self.taskDef)
        self.assertTrue(mock.called)
        mock.assert_called_with([self.taskDef])
    
    @patch.object(MetadataResourceApi, 'update_task_def')
    def test_updateTaskDef(self, mock):
        self.metadata_client.update_task_def(self.taskDef)
        self.assertTrue(mock.called)
        mock.assert_called_with(self.taskDef)
    
    @patch.object(MetadataResourceApi, 'unregister_task_def')
    def test_unregisterTaskDef(self, mock):
        self.metadata_client.unregister_task_def(TASK_NAME)
        self.assertTrue(mock.called)
        mock.assert_called_with(TASK_NAME)

    @patch.object(MetadataResourceApi, 'get_task_def')
    def test_getTaskDef(self, mock):
        mock.return_value = self.taskDef
        taskDefinition = self.metadata_client.get_task_def(TASK_NAME)
        self.assertEqual(taskDefinition, self.taskDef)
        mock.assert_called_with(TASK_NAME)

    @patch.object(MetadataResourceApi, 'get_task_defs')
    def test_getAllTaskDefs(self, mock):
        taskDef2 = TaskDef("ut_task2")
        mock.return_value = [self.taskDef, taskDef2]
        tasks = self.metadata_client.get_all_task_defs()
        self.assertEqual(len(tasks), 2)

    @patch.object(TagsApi, 'add_workflow_tag')
    def test_addWorkflowTag(self, mock):
        self.metadata_client.add_workflow_tag(self.wfTagObj, WORKFLOW_NAME)
        mock.assert_called_with(self.wfTagObj, WORKFLOW_NAME)

    @patch.object(TagsApi, 'delete_workflow_tag')
    def test_deleteWorkflowTag(self, mock):
        wfTagOStr = TagString("test", "METADATA", "val")
        self.metadata_client.delete_workflow_tag(self.wfTagObj, WORKFLOW_NAME)
        mock.assert_called_with(wfTagOStr, WORKFLOW_NAME)

    @patch.object(TagsApi, 'set_workflow_tags')
    def test_setWorkflowTags(self, mock):
        wfTagObj2 = MetadataTag("test2", "val2")
        wfTagObjs = [self.wfTagObj, wfTagObj2]
        self.metadata_client.set_workflow_tags(wfTagObjs, WORKFLOW_NAME)
        mock.assert_called_with(wfTagObjs, WORKFLOW_NAME)

    @patch.object(TagsApi, 'get_workflow_tags')
    def test_getWorkflowTags(self, mock):
        wfTagObj2 = MetadataTag("test2", "val2")
        mock.return_value = [self.wfTagObj, wfTagObj2]
        tags = self.metadata_client.get_workflow_tags(WORKFLOW_NAME)
        mock.assert_called_with(WORKFLOW_NAME)
        self.assertEqual(len(tags), 2)

    @patch.object(TagsApi, 'add_task_tag')
    def test_add_task_tag(self, mock):
        taskTag = MetadataTag("tag1", "val1")
        self.metadata_client.add_task_tag(taskTag, TASK_NAME)
        mock.assert_called_with(taskTag, TASK_NAME)

    @patch.object(TagsApi, 'delete_task_tag')
    def test_delete_task_tag(self, mock):
        taskTag = MetadataTag("tag1", "val1")
        taskTagStr = TagString("tag1", "METADATA", "val1")
        self.metadata_client.delete_task_tag(taskTag, TASK_NAME)
        mock.assert_called_with(taskTagStr, TASK_NAME)

    @patch.object(TagsApi, 'set_task_tags')
    def test_set_task_tags(self, mock):
        taskTag1 = MetadataTag("tag1", "val1")
        taskTag2 = MetadataTag("tag2", "val2")
        taskTagObjs = [taskTag1, taskTag2]
        self.metadata_client.set_task_tags(taskTagObjs, TASK_NAME)
        mock.assert_called_with(taskTagObjs, TASK_NAME)

    @patch.object(TagsApi, 'get_task_tags')
    def test_get_task_tags(self, mock):
        taskTag1 = MetadataTag("tag1", "val1")
        taskTag2 = MetadataTag("tag2", "val2")
        mock.return_value = [taskTag1, taskTag2]
        tags = self.metadata_client.get_task_tags(TASK_NAME)
        mock.assert_called_with(TASK_NAME)
        self.assertEqual(len(tags), 2)

    @patch.object(TagsApi, 'get_workflow_tags')
    @patch.object(TagsApi, 'add_workflow_tag')
    def test_set_workflow_rate_limit(self, mockSet, mockRemove):
        mockRemove.return_value = []
        rateLimitTag = RateLimitTag(WORKFLOW_NAME, 5)
        self.metadata_client.set_workflow_rate_limit(5, WORKFLOW_NAME)
        mockRemove.assert_called_with(WORKFLOW_NAME)
        mockSet.assert_called_with(rateLimitTag, WORKFLOW_NAME)

    @patch.object(TagsApi, 'get_workflow_tags')
    def test_get_workflow_rate_limit(self, mock):
        metadataTag = MetadataTag("test", "val")
        rateLimitTag = RateLimitTag(WORKFLOW_NAME, 5)
        mock.return_value = [metadataTag, rateLimitTag]
        rateLimit = self.metadata_client.get_workflow_rate_limit(WORKFLOW_NAME)
        self.assertEqual(rateLimit, 5)

    @patch.object(TagsApi, 'get_workflow_tags')
    def test_get_workflow_rate_limit_not_set(self, mock):
        mock.return_value = []
        rateLimit = self.metadata_client.get_workflow_rate_limit(WORKFLOW_NAME)
        mock.assert_called_with(WORKFLOW_NAME)
        self.assertIsNone(rateLimit)

    @patch.object(OrkesMetadataClient, 'get_workflow_rate_limit')
    @patch.object(TagsApi, 'delete_workflow_tag')
    def test_remove_workflow_rate_limit(self, patchedTagsApi, patchedMetadataClient):
        patchedMetadataClient.return_value = 5
        self.metadata_client.remove_workflow_rate_limit(WORKFLOW_NAME)
        rateLimitTag = RateLimitTag(WORKFLOW_NAME, 5)
        patchedTagsApi.assert_called_with(rateLimitTag, WORKFLOW_NAME)

