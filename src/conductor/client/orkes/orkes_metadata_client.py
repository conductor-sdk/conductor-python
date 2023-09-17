from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.rest import ApiException
from conductor.client.http.api_client import ApiClient

from conductor.client.metadata_client import MetadataClient
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.models.tag_string import TagString
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.http.api.tags_api import TagsApi
from conductor.client.orkes.models.metadata_tag import MetadataTag

class OrkesMetadataClient(MetadataClient):
    def __init__(self, configuration: Configuration):
        api_client = ApiClient(configuration)
        self.metadataResourceApi = MetadataResourceApi(api_client)
        self.tagsApi = TagsApi(api_client)
        
    def registerWorkflowDef(self, workflowDef: WorkflowDef, overwrite: Optional[bool] = True):
        self.metadataResourceApi.create(workflowDef, overwrite=overwrite)

    def updateWorkflowDef(self, workflowDef: WorkflowDef, overwrite: Optional[bool] = True):
        self.metadataResourceApi.update1([workflowDef], overwrite=overwrite)

    def unregisterWorkflowDef(self, name: str, version: int):
        self.metadataResourceApi.unregister_workflow_def(name, version)

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
        self.metadataResourceApi.register_task_def([taskDef])

    def updateTaskDef(self, taskDef: TaskDef):
        self.metadataResourceApi.update_task_def(taskDef)

    def unregisterTaskDef(self, taskType: str):
        self.metadataResourceApi.unregister_task_def(taskType)

    def getTaskDef(self, taskType: str) -> TaskDef:
        return self.metadataResourceApi.get_task_def(taskType)

    def getAllTaskDefs(self) -> List[TaskDef]:
        return self.metadataResourceApi.get_task_defs()
        
    def addWorkflowMetadataTag(self, tag: MetadataTag, workflowName: str):
        self.tagsApi.add_workflow_tag(tag, workflowName)

    def deleteWorkflowMetadataTag(self, tag: MetadataTag, workflowName: str):
        tagStr = TagString(tag.key, tag.type, tag.value)
        self.tagsApi.delete_workflow_tag(tagStr, workflowName)

    def getWorkflowMetadataTags(self, workflowName: str) -> List[MetadataTag]:
        return self.tagsApi.get_workflow_tags(workflowName)

    def setWorkflowMetadataTags(self, tags: List[MetadataTag], workflowName: str):
        self.tagsApi.set_workflow_tags(tags, workflowName)

    def addTaskTag(self, tag: MetadataTag, taskName: str):
        self.tagsApi.add_task_tag(tag, taskName)
    
    def deleteTaskTag(self, tag: MetadataTag, taskName: str):
        tagStr = TagString(tag.key, tag.type, tag.value)
        self.tagsApi.delete_task_tag(tagStr, taskName)

    def getTaskTags(self, taskName: str) -> List[MetadataTag]:
        return self.tagsApi.get_task_tags(taskName)
        
    def setTaskTags(self, tags: List[MetadataTag], taskName: str):
        self.tagsApi.set_task_tags(tags, taskName)
            