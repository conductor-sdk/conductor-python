from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient

from conductor.client.metadata_client import MetadataClient
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi

class OrkesMetadataClient(MetadataClient):
    def __init__(self, configuration: Configuration):
        api_client = ApiClient(configuration)
        self.metadataResourceApi = MetadataResourceApi(api_client)
        
    def registerWorkflowDef(self, workflowDef: WorkflowDef, overwrite: bool):
        pass

    def unregisterWorkflowDef(self, workflowId: str):
        pass

    def updateWorkflowDef(self):
        pass

    def getWorkflowDef(self, name: str, version: Optional[int] = None) -> WorkflowDef:
        if version:
            return self.metadataResourceApi.get(name, version=version)
        
        return self.metadataResourceApi.get(name)

    def getAllWorkflowDefs(self) -> List[WorkflowDef]:
        return self.metadataResourceApi.get_all_workflows()

    def registerTaskDef(self):
        pass

    def unregisterTaskDef(self):
        pass

    def updateTaskDef(self):
        pass

    def getTaskDef(self):
        pass

    def getAllTaskDefs(self):
        pass

    def getTags(self):
        pass
    
    def getWorkflowTags(self):
        pass
    
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