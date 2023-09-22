from abc import ABC, abstractmethod
from typing import List
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_exec_log import TaskExecLog

class TaskClientInterface(ABC):
    @abstractmethod
    def pollTask(self, taskType: str, workerId: str, domain: str) -> Task:
        pass

    @abstractmethod
    def updateTask(self, taskResult: TaskResult):
        pass

    @abstractmethod
    def getTask(self, taskId: str):
        pass

    @abstractmethod
    def addTaskLog(self, taskId: str, logMessage: str):
        pass

    @abstractmethod
    def getTaskLogs(self, taskId: str) -> List[TaskExecLog>]:
        pass

    @abstractmethod
    def getPollData(self, taskType: str) -> List[WorkflowDef]:
        pass

