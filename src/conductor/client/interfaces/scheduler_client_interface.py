from abc import ABC, abstractmethod
from typing import Optional, List
from conductor.client.http.models.workflow_schedule import WorkflowSchedule
from conductor.client.http.models.save_schedule_request import SaveScheduleRequest
from conductor.client.http.models.search_result_workflow_schedule_execution_model import SearchResultWorkflowScheduleExecutionModel
from conductor.client.orkes.models.metadata_tag import MetadataTag

class SchedulerClientInterface(ABC):
    @abstractmethod
    def saveSchedule(self, saveScheduleRequest: SaveScheduleRequest):
        pass
    
    @abstractmethod
    def getSchedule(self, name: str) -> (Optional[WorkflowSchedule], str):
        pass
    
    @abstractmethod
    def getAllSchedules(self, workflowName: Optional[str] = None) -> List[WorkflowSchedule]:
        pass
    
    @abstractmethod
    def getNextFewScheduleExecutionTimes(self,
        cronExpression: str,
        scheduleStartTime: Optional[int] = None,
        scheduleEndTime: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[int]:
        pass

    @abstractmethod
    def deleteSchedule(self, name: str):
        pass

    @abstractmethod
    def pauseSchedule(self, name: str):
        pass
    
    @abstractmethod
    def pauseAllSchedules(self):
        pass
    
    @abstractmethod
    def resumeSchedule(self, name: str):
        pass
    
    @abstractmethod
    def resumeAllSchedules(self):
        pass

    @abstractmethod
    def searchScheduleExecutions(self,
        start: Optional[int] = None,
        size: Optional[int] = None,
        sort: Optional[str] = None,
        freeText: Optional[str] = None,
        query: Optional[str] = None,
    ) -> SearchResultWorkflowScheduleExecutionModel:
        pass
    
    @abstractmethod
    def requeueAllExecutionRecords(self):
        pass

    @abstractmethod
    def setSchedulerTags(self, tags: List[MetadataTag], name: str):
        pass

    @abstractmethod
    def getSchedulerTags(self, name: str) -> List[MetadataTag]:
        pass
        
    @abstractmethod
    def deleteSchedulerTags(self, tags: List[MetadataTag], name: str) -> List[MetadataTag]:
        pass

