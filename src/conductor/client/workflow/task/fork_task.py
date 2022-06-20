from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.workflow.task.join_task import JoinTask
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing import List
from typing_extensions import Self


class ForkTask(TaskInterface):
    _forked_tasks: List[List[TaskInterface]]
    _join_task: JoinTask

    def __init__(self, task_ref_name: str, forked_tasks: List[List[TaskInterface]]) -> Self:
        super().__init__(task_ref_name, TaskType.FORK_JOIN)
        self._forked_tasks = forked_tasks
        self._join_task = JoinTask(task_ref_name + '_join')

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.fork_tasks = []
        for inner_forked_tasks in self._forked_tasks:
            converted_inner_forked_tasks = []
            for inner_forked_task in inner_forked_tasks:
                converted_inner_forked_tasks.append(
                    inner_forked_task.to_workflow_task()
                )
            workflow.fork_tasks.append(converted_inner_forked_tasks)
        workflow.join_on = self._join_task.to_workflow_task()
        return workflow
