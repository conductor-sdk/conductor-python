import logging
import unittest

from unittest.mock import Mock, patch
from conductor.client.http.orkes_metadata_client import OrkesMetadataClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.workflow_def import WorkflowDef

WORKFLOW_NAME = 'ut_wf'

class TestOrkesMetadataClient(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.metadata_client = OrkesMetadataClient(configuration)
        
    def setUp(self):
        self.workflowDef = WorkflowDef(name=WORKFLOW_NAME, version=1)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "metadataResourceApi is not of type MetadataResourceApi"
        self.assertIsInstance(self.metadata_client.metadataResourceApi, MetadataResourceApi, message)

    @patch.object(MetadataResourceApi, 'get')
    def test_getWorkflowDef_without_version(self, mock):
        mock.return_value = self.workflowDef
        wf = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        self.assertEqual(wf, self.workflowDef)
        self.assertTrue(mock.called)
        mock.assert_called_with(WORKFLOW_NAME)
    
    @patch.object(MetadataResourceApi, 'get')
    def test_getWorkflowDef_with_version(self, mock):
        mock.return_value = self.workflowDef
        wf = self.metadata_client.getWorkflowDef(WORKFLOW_NAME, 1)
        self.assertEqual(wf, self.workflowDef)
        mock.assert_called_with(WORKFLOW_NAME, version=1)

    @patch.object(MetadataResourceApi, 'get_all_workflows')
    def test_getAllWorkflowDefs(self, mock):
        workflowDef2 = WorkflowDef(name='ut_wf_2', version=1)
        mock.return_value = [self.workflowDef, workflowDef2]
        wfs = self.metadata_client.getAllWorkflowDefs()
        self.assertEqual(len(wfs), 2)