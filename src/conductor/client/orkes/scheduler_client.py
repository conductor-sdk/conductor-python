from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.rest import ApiException
from conductor.client.http.api_client import ApiClient
from conductor.client.http.models.tag_string import TagString
from conductor.client.http.api.scheduler_resource_api import SchedulerResourceApi
from conductor.client.orkes.api.tags_api import TagsApi
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.http.models.workflow_schedule import WorkflowSchedule
from conductor.client.interfaces.scheduler_client_interface import SchedulerClientInterface
from conductor.client.http.models.save_schedule_request import SaveScheduleRequest
from conductor.client.http.models.search_result_workflow_schedule_execution_model import SearchResultWorkflowScheduleExecutionModel

class SchedulerClient(SchedulerClientInterface):
    def __init__(self, configuration: Configuration):
        api_client = ApiClient(configuration)
        self.schedulerResourceApi = SchedulerResourceApi(api_client)
        self.tagsApi = TagsApi(api_client)
        
    def saveSchedule(self, saveScheduleRequest: SaveScheduleRequest):
        self.schedulerResourceApi.save_schedule(saveScheduleRequest)
    
    def getSchedule(self, name: str) -> (Optional[WorkflowSchedule], str):
        schedule, error = None, None
        try:
            schedule = self.schedulerResourceApi.get_schedule(name)
        except ApiException as e:
            message = e.reason if e.reason else e.body
            error = "Error in fetching schedule: " + message
        return schedule, error

    def getAllSchedules(self, workflowName: Optional[str] = None) -> List[WorkflowSchedule]:
        kwargs = {}
        if workflowName:
            kwargs.update({"workflow_name": workflowName})

        return self.schedulerResourceApi.get_all_schedules(**kwargs)

    def getNextFewScheduleExecutionTimes(self,
        cronExpression: str,
        scheduleStartTime: Optional[int] = None,
        scheduleEndTime: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[int]:
        kwargs = {}
        if scheduleStartTime:
            kwargs.update({"schedule_start_time": scheduleStartTime})
        if scheduleEndTime:
            kwargs.update({"schedule_end_time": scheduleEndTime})
        if limit:
            kwargs.update({"limit": limit})
        return self.schedulerResourceApi.get_next_few_schedules(cronExpression, **kwargs)

    def deleteSchedule(self, name: str):
        self.schedulerResourceApi.delete_schedule(name)

    def pauseSchedule(self, name: str):
        self.schedulerResourceApi.pause_schedule(name)
    
    def pauseAllSchedules(self):
        self.schedulerResourceApi.pause_all_schedules()

    def resumeSchedule(self, name: str):
        self.schedulerResourceApi.resume_schedule(name)
    
    def resumeAllSchedules(self):
        self.schedulerResourceApi.resume_all_schedules()
    
    def searchScheduleExecutions(self,
        start: Optional[int] = None,
        size: Optional[int] = None,
        sort: Optional[str] = None,
        freeText: Optional[str] = None,
        query: Optional[str] = None,
    ) -> SearchResultWorkflowScheduleExecutionModel:
        kwargs = {}
        if start:
            kwargs.update({"start": start})
        if size:
            kwargs.update({"size": size})
        if sort:
            kwargs.update({"sort": sort})
        if freeText:
            kwargs.update({"freeText": freeText})
        if query:
            kwargs.update({"query": query})
        return self.schedulerResourceApi.search_v21(**kwargs)
    
    def requeueAllExecutionRecords(self):
        self.schedulerResourceApi.requeue_all_execution_records()
    
    def setSchedulerTags(self, tags: List[MetadataTag], name: str):
        self.schedulerResourceApi.put_tag_for_schedule(tags, name)

    def getSchedulerTags(self, name: str) -> List[MetadataTag]:
        return self.schedulerResourceApi.get_tags_for_schedule(name)
        
    def deleteSchedulerTags(self, tags: List[MetadataTag], name: str)  -> List[MetadataTag]:
        self.schedulerResourceApi.delete_tag_for_schedule(tags, name)
