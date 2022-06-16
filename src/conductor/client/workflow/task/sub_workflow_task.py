from __future__ import annotations
from conductor.client.http.models.sub_workflow_params import SubWorkflowParams
from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing import Dict


class SubWorkflowTask(TaskInterface):
    _workflow_name: str
    _version: int
    _task_to_domain_map: Dict[str, str]

    def __init__(self, task_ref_name: str, workflow_name: str = None, version: int = None, task_to_domain_map: Dict[str, str] = None) -> SubWorkflowTask:
        super().__init__(task_ref_name, TaskType.SUB_WORKFLOW)
        self._workflow_name = workflow_name
        self._version = version
        self._task_to_domain_map = task_to_domain_map

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.sub_workflow_param = SubWorkflowParams(
            name=self._workflow_name,
            version=self._version,
            task_to_domain=self._task_to_domain_map,
        )
        return workflow


class InlineSubWorkflowTask(TaskInterface):
    _workflow: ConductorWorkflow

    def __init__(self, task_ref_name: str, workflow: ConductorWorkflow) -> InlineSubWorkflowTask:
        super().__init__(task_ref_name, TaskType.SUB_WORKFLOW)
        self._workflow = workflow

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.sub_workflow_param = SubWorkflowParams(
            name=self._workflow.name,
            version=self._workflow.version,
            workflow_definition=self._workflow.to_workflow_def(),
        )
        return workflow
