from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.rest import ApiException
from conductor.client.http.api_client import ApiClient

from conductor.client.metadata_client import MetadataClient
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.workflow_tag import WorkflowTag
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi

class OrkesMetadataClient(MetadataClient):
    def __init__(self, configuration: Configuration):
        api_client = ApiClient(configuration)
        self.metadataResourceApi = MetadataResourceApi(api_client)
        
    def registerWorkflowDef(self, workflowDef: WorkflowDef, overwrite: Optional[bool] = True):
        self.metadataResourceApi.create(workflowDef, overwrite)

    def unregisterWorkflowDef(self, name: str, version: int):
        self.metadataResourceApi.unregister_workflow_def(name, version)

    def updateWorkflowDef(self):
        pass

    def getWorkflowDef(self, name: str, version: Optional[int] = None) -> (Optional[WorkflowDef], str):
        workflow = None
        error = None
        try:
            if version:
                workflow = self.metadataResourceApi.get(name, version=version)
            else:
                workflow = self.metadataResourceApi.get(name)
        except ApiException as e:
            message = e.reason if e.reason else e.body
            error = "Error in fetching workflow: " + message
            
        return workflow, error

    def getAllWorkflowDefs(self) -> List[WorkflowDef]:
        return self.metadataResourceApi.get_all_workflows()

    def registerTaskDef(self, taskDef: TaskDef):
        self.metadataResourceApi.register_task_def(taskDef)

    def updateTaskDef(self, taskDef: TaskDef):
        self.metadataResourceApi.update_task_def(taskDef)

    def unregisterTaskDef(self, taskType: str):
        self.metadataResourceApi.unregister_task_def(taskType)

    def getTaskDef(self, taskType: str) -> TaskDef:
        return self.metadataResourceApi.get_task_def(taskType)

    def getAllTaskDefs(self) -> List[TaskDef]:
        return self.metadataResourceApi.get_task_defs()

    def getTags(self):
        pass
    
    def getWorkflowTags(self, workflowName: str) -> List[WorkflowTag]:
        return self.metadataResourceApi.get_workflow_metadata(workflowName)
    
    def setWorkflowTags(self):
        pass
    
    def deleteWorkflowTags(self):
        pass

    def getTaskTags(self):
        pass
    
    def setTaskTags(self):
        pass
    
    def deleteTaskTags(self):
        pass