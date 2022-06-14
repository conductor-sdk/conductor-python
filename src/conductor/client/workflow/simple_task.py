from src.conductor.client.workflow.task_type import TaskType
from task import TaskInterface


class Simple(TaskInterface):
    def __init__(self, task_def_name: str, task_reference_name: str):
        super().__init__(task_reference_name, TaskType.SIMPLE)
        self.name = task_def_name
