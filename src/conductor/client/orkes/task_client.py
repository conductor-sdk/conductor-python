from abc import ABC, abstractmethod
from typing import List
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_exec_log import TaskExecLog
from conductor.client.interfaces.task_client_interface import TaskClientInterface

class TaskClient(TaskClientInterface):
    def pollTask(self, taskType: str, workerId: str, domain: str) -> Task:
        pass

    def updateTask(self, taskResult: TaskResult):
        pass

    def getTask(self, taskId: str):
        pass

    def addTaskLog(self, taskId: str, logMessage: str):
        pass

    def getTaskLogs(self, taskId: str) -> List[TaskExecLog>]:
        pass

    def getPollData(self, taskType: str) -> List[WorkflowDef]:
        pass

