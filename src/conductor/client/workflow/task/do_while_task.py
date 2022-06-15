from __future__ import annotations
from typing import List
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.http.models.workflow_task import WorkflowTask
from task import TaskInterface


class DoWhileTask(TaskInterface):
    _loop_condition: str
    _loop_over: List[TaskInterface]

    # termination_condition is a Javascript expression that evaluates to True or False
    def __init__(self, task_ref_name: str, termination_condition: str, tasks: List[TaskInterface]) -> DoWhileTask:
        super().__init__(task_ref_name, TaskType.DO_WHILE)
        self._loop_condition = termination_condition
        self._loop_over = tasks

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.loop_condition = self._loop_condition
        workflow.loop_over = self.get_task_interface_list_as_workflow_task_list(
            self._loop_over)
        return workflow


class LoopTask(DoWhileTask):
    def __init__(self, task_ref_name: str, iterations: int, tasks: List[TaskInterface]) -> DoWhileTask:
        super().__init__(
            task_ref_name,
            self.get_for_loop_condition(task_ref_name, iterations),
            tasks,
        )

    @staticmethod
    def get_for_loop_condition(task_ref_name: str, iterations: int) -> str:
        return "if ( $.%s['iteration'] < $.%d ) { true; } else { false; }" % task_ref_name, iterations
