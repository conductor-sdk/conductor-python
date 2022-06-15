from __future__ import annotations
from typing import Dict
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.sub_workflow_params import SubWorkflowParams
from conductor.client.workflow.task.task import TaskInterface


class SubWorkflowTask(TaskInterface):
    _workflow_name: str
    _version: int
    _task_to_domain_map: Dict[str, str]
    _workflow_definition: WorkflowDef

    def __init__(self, task_ref_name: str, workflow_name: str, workflow_definition: WorkflowDef = None) -> SubWorkflowTask:
        super().__init__(task_ref_name, TaskType.SUB_WORKFLOW)
        self._workflow_name = workflow_name
        self._workflow_definition = workflow_definition
        self._version = None

    def version(self, version: int) -> SubWorkflowTask:
        self._version = version
        return self

    def task_to_domain_map(self, task_to_domain_map: Dict[str, str]) -> SubWorkflowTask:
        self._task_to_domain_map = task_to_domain_map
        return self

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.sub_workflow_param = SubWorkflowParams(
            name=self._workflow_name,
            version=self._version,
            task_to_domain=self._task_to_domain_map,
            workflow_definition=self._workflow_definition,
        )
        return workflow


class InlineSubWorkflowTask(SubWorkflowTask):
    def __init__(self, task_ref_name: str, workflow: ConductorWorkflow) -> SubWorkflowTask:
        super().__init__(
            task_ref_name=task_ref_name,
            workflow_name=workflow._name,
            version=workflow._version
        )
