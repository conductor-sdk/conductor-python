from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask

import json

WORKFLOW_NAME = 'IntegrationTestMetadataClientWf'

class TestOrkesClients:
    def __init__(self, configuration: Configuration):
        self.workflow_executor = WorkflowExecutor(configuration)
        self.metadata_client = OrkesMetadataClient(configuration)
        self.workflow = ConductorWorkflow(
            executor=self.workflow_executor,
            name=WORKFLOW_NAME,
            description='Test Create Workflow',
            version=1
        )
        self.workflow.input_parameters(["a", "b"])
        self.workflow >> SimpleTask("simple_task", "simple_task_ref")
        self.workflowDef = self.workflow.to_workflow_def()
        
    def run(self) -> None:
        self.__test_register_workflow_definition()
        self.__test_get_workflow_definition()
        self.__test_update_workflow_definition()
        self.__test_unregister_workflow_definition()
        self.__test_get_invalid_workflow_definition()

    def __test_register_workflow_definition(self):
        self.metadata_client.registerWorkflowDef(self.workflowDef, True)

    def __test_get_workflow_definition(self):
        wfDef, _ = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        assert wfDef.name == self.workflowDef.name
        assert len(wfDef.tasks) == 1

    def __test_update_workflow_definition(self):
        self.workflow >> SimpleTask("simple_task", "simple_task_ref_2")
        updatedWorkflowDef = self.workflow.to_workflow_def()
        self.metadata_client.updateWorkflowDef(updatedWorkflowDef, True)
        wfDef, _ = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        assert len(wfDef.tasks) == 2

    def __test_unregister_workflow_definition(self):
        self.metadata_client.unregisterWorkflowDef(WORKFLOW_NAME, 1)
        
    def __test_get_invalid_workflow_definition(self):
        wfDef, error = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        assert wfDef == None
        assert error != None

