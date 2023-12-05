"""Orkes Scheduler Client

The class in this module allows management of schedules.
"""

from typing import List, Optional

from conductor.client.exceptions.api_exception_handler import (
    api_exception_handler, for_all_methods)
from conductor.client.http.models.save_schedule_request import \
    SaveScheduleRequest
from conductor.client.http.models.search_result_workflow_schedule_execution_model import \
    SearchResultWorkflowScheduleExecutionModel
from conductor.client.http.models.workflow_schedule import WorkflowSchedule
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.scheduler_client import SchedulerClient


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesSchedulerClient(OrkesBaseClient, SchedulerClient):
    """
    A class to manage schedules. Supports searching, scheduler tag management,
    pausing and resuming schedules along with bulk actions.
    """

    def save_schedule(self, save_schedule_request: SaveScheduleRequest):
        self.scheduler_resource_api.save_schedule(save_schedule_request)

    def get_schedule(self, name: str) -> WorkflowSchedule:
        return self.scheduler_resource_api.get_schedule(name)

    def get_all_schedules(
        self, workflow_name: Optional[str] = None
    ) -> List[WorkflowSchedule]:
        kwargs = {}
        if workflow_name:
            kwargs.update({"workflow_name": workflow_name})

        return self.scheduler_resource_api.get_all_schedules(**kwargs)

    def get_next_few_schedule_execution_times(
        self,
        cron_expression: str,
        schedule_start_time: Optional[int] = None,
        schedule_end_time: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[int]:
        kwargs = {}
        if schedule_start_time:
            kwargs.update({"schedule_start_time": schedule_start_time})
        if schedule_end_time:
            kwargs.update({"schedule_end_time": schedule_end_time})
        if limit:
            kwargs.update({"limit": limit})
        return self.scheduler_resource_api.get_next_few_schedules(
            cron_expression, **kwargs
        )

    def delete_schedule(self, name: str):
        self.scheduler_resource_api.delete_schedule(name)

    def pause_schedule(self, name: str):
        self.scheduler_resource_api.pause_schedule(name)

    def pause_all_schedules(self):
        self.scheduler_resource_api.pause_all_schedules()

    def resume_schedule(self, name: str):
        self.scheduler_resource_api.resume_schedule(name)

    def resume_all_schedules(self):
        self.scheduler_resource_api.resume_all_schedules()

    def search_schedule_executions(
        self,
        start: Optional[int] = None,
        size: Optional[int] = None,
        sort: Optional[str] = None,
        free_text: Optional[str] = None,
        query: Optional[str] = None,
    ) -> SearchResultWorkflowScheduleExecutionModel:
        kwargs = {}
        if start:
            kwargs.update({"start": start})
        if size:
            kwargs.update({"size": size})
        if sort:
            kwargs.update({"sort": sort})
        if free_text:
            kwargs.update({"freeText": free_text})
        if query:
            kwargs.update({"query": query})
        return self.scheduler_resource_api.search_v21(**kwargs)

    def requeue_all_execution_records(self):
        self.scheduler_resource_api.requeue_all_execution_records()

    def set_scheduler_tags(self, tags: List[MetadataTag], name: str):
        self.scheduler_resource_api.put_tag_for_schedule(tags, name)

    def get_scheduler_tags(self, name: str) -> List[MetadataTag]:
        return self.scheduler_resource_api.get_tags_for_schedule(name)

    def delete_scheduler_tags(
        self, tags: List[MetadataTag], name: str
    ) -> List[MetadataTag]:
        self.scheduler_resource_api.delete_tag_for_schedule(tags, name)
