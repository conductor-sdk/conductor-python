"""Orkes Metadata Client

The class in this module allows management of Orkes Metadata.
"""

from typing import List, Optional

from conductor.client.exceptions.api_exception_handler import (
    api_exception_handler, for_all_methods)
from conductor.client.http.models.tag_string import TagString
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.metadata_client import MetadataClient
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.models.ratelimit_tag import RateLimitTag
from conductor.client.orkes.orkes_base_client import OrkesBaseClient


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesMetadataClient(OrkesBaseClient, MetadataClient):
    """
    A class to manage Orkes metadata that constitutes workflow definitions and
    task definitions.
    """

    def register_workflow_def(
        self, workflow_def: WorkflowDef, overwrite: Optional[bool] = True
    ):
        self.metadata_resource_api.create(workflow_def, overwrite=overwrite)

    def update_workflow_def(
        self, workflow_def: WorkflowDef, overwrite: Optional[bool] = True
    ):
        self.metadata_resource_api.update1([workflow_def], overwrite=overwrite)

    def unregister_workflow_def(self, name: str, version: int):
        self.metadata_resource_api.unregister_workflow_def(name, version)

    def get_workflow_def(self, name: str, version: Optional[int] = None) -> WorkflowDef:
        workflow = None
        if version:
            workflow = self.metadata_resource_api.get(name, version=version)
        else:
            workflow = self.metadata_resource_api.get(name)

        return workflow

    def get_all_workflow_defs(self) -> List[WorkflowDef]:
        return self.metadata_resource_api.get_all_workflows()

    def register_task_def(self, task_def: TaskDef):
        self.metadata_resource_api.register_task_def([task_def])

    def update_task_def(self, task_def: TaskDef):
        self.metadata_resource_api.update_task_def(task_def)

    def unregister_task_def(self, task_type: str):
        self.metadata_resource_api.unregister_task_def(task_type)

    def get_task_def(self, task_type: str) -> TaskDef:
        return self.metadata_resource_api.get_task_def(task_type)

    def get_all_task_defs(self) -> List[TaskDef]:
        return self.metadata_resource_api.get_task_defs()

    def add_workflow_tag(self, tag: MetadataTag, workflow_name: str):
        self.tags_api.add_workflow_tag(tag, workflow_name)

    def delete_workflow_tag(self, tag: MetadataTag, workflow_name: str):
        tag_str = TagString(tag.key, tag.type, tag.value)
        self.tags_api.delete_workflow_tag(tag_str, workflow_name)

    def get_workflow_tags(self, workflow_name: str) -> List[MetadataTag]:
        return self.tags_api.get_workflow_tags(workflow_name)

    def set_workflow_tags(self, tags: List[MetadataTag], workflow_name: str):
        self.tags_api.set_workflow_tags(tags, workflow_name)

    def add_task_tag(self, tag: MetadataTag, task_name: str):
        self.tags_api.add_task_tag(tag, task_name)

    def delete_task_tag(self, tag: MetadataTag, task_name: str):
        tag_str = TagString(tag.key, tag.type, tag.value)
        self.tags_api.delete_task_tag(tag_str, task_name)

    def get_task_tags(self, task_name: str) -> List[MetadataTag]:
        return self.tags_api.get_task_tags(task_name)

    def set_task_tags(self, tags: List[MetadataTag], task_name: str):
        self.tags_api.set_task_tags(tags, task_name)

    def set_workflow_rate_limit(self, rate_limit: int, workflow_name: str):
        self.remove_workflow_rate_limit(workflow_name)
        rate_limit_tag = RateLimitTag(workflow_name, rate_limit)
        self.tags_api.add_workflow_tag(rate_limit_tag, workflow_name)

    def get_workflow_rate_limit(self, workflow_name: str) -> Optional[int]:
        tags = self.tags_api.get_workflow_tags(workflow_name)
        for tag in tags:
            if tag.type == "RATE_LIMIT" and tag.key == workflow_name:
                return tag.value

        return None

    def remove_workflow_rate_limit(self, workflow_name: str):
        current_rate_limit = self.get_workflow_rate_limit(workflow_name)
        if current_rate_limit:
            rate_limit_tag = RateLimitTag(workflow_name, current_rate_limit)
            self.tags_api.delete_workflow_tag(rate_limit_tag, workflow_name)
