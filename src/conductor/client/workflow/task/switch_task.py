from __future__ import annotations
from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.workflow.task.task import TaskInterface, get_task_interface_list_as_workflow_task_list
from conductor.client.workflow.task.task_type import TaskType
from enum import Enum
from typing import Dict, List


class EvaluatorType(str, Enum):
    JAVASCRIPT = "javascript",
    VALUE_PARAM = "value-param"


class SwitchTask(TaskInterface):
    _decision_cases: Dict[str, List[TaskInterface]]
    _default_case: List[TaskInterface]
    _expression: str
    _use_javascript: bool
    _evaluator_type: EvaluatorType

    def __init__(self, task_ref_name: str, case_expression: str, use_javascript: bool = False) -> SwitchTask:
        super().__init__(
            task_reference_name=task_ref_name,
            task_type=TaskType.SWITCH,
        )
        self._decision_cases = {}
        self._expression = case_expression
        self._use_javascript = use_javascript

    def switch_case(self, case_name: str, tasks: List[TaskInterface]) -> SwitchTask:
        self._decision_cases[case_name] = tasks
        return self

    def default_case(self, tasks: List[TaskInterface]) -> SwitchTask:
        self._default_case = tasks
        return self

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        if self._use_javascript:
            workflow.evaluator_type = EvaluatorType.JAVASCRIPT
        else:
            workflow.evaluator_type = EvaluatorType.VALUE_PARAM
            workflow.input_parameters['switchCaseValue'] = self._expression
            workflow.expression = 'switchCaseValue'
        workflow.decision_cases = {}
        for case_value, tasks in self._decision_cases.items():
            workflow.decision_cases[case_value] = get_task_interface_list_as_workflow_task_list(
                *tasks,
            )
        workflow.default_case = get_task_interface_list_as_workflow_task_list(
            self._default_case
        )
        return workflow
