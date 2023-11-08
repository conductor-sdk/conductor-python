from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_exec_log import TaskExecLog
from conductor.client.task_client import TaskClient
from conductor.client.http.models.workflow import Workflow
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.exceptions.api_exception_handler import api_exception_handler, for_all_methods

@for_all_methods(api_exception_handler, ["__init__"])
class OrkesTaskClient(OrkesBaseClient, TaskClient):
    def __init__(self, configuration: Configuration):
        super(OrkesTaskClient, self).__init__(configuration)

    def pollTask(self, taskType: str, workerId: Optional[str] = None, domain: Optional[str] = None) -> Optional[Task]:
        kwargs = {}
        if workerId:
            kwargs.update({"workerid": workerId})
        if domain:
            kwargs.update({"domain": domain})

        return self.taskResourceApi.poll(taskType, **kwargs)

    def batchPollTasks(
        self,
        taskType: str,
        workerId: Optional[str] = None,
        count: Optional[int] = None,
        timeoutInMillisecond: Optional[int] = None,
        domain: Optional[str] = None
    ) -> List[Task]:
        kwargs = {}
        if workerId:
            kwargs.update({"workerid": workerId})
        if count:
            kwargs.update({"count": count})
        if timeoutInMillisecond:
            kwargs.update({"timeout": timeoutInMillisecond})
        if domain:
            kwargs.update({"domain": domain})

        return self.taskResourceApi.batch_poll(taskType, **kwargs)

    def getTask(self, taskId: str) -> Task:
        return self.taskResourceApi.get_task(taskId)

    def updateTask(self, taskResult: TaskResult) -> str:
        return self.taskResourceApi.update_task(taskResult)

    def updateTaskByRefName(
        self,
        workflowId: str,
        taskRefName: str,
        status: str,
        output: object,
        workerId: Optional[str] = None
    ) -> str:
        body = { "result": output }
        kwargs = {}
        if workerId:
            kwargs.update({"workerid": workerId})
        return self.taskResourceApi.update_task1(body, workflowId, taskRefName, status, **kwargs)
    
    def updateTaskSync(
        self,
        workflowId: str,
        taskRefName: str,
        status: str,
        output: object,
        workerId: Optional[str] = None
    ) -> Workflow:
        body = { "result": output }
        kwargs = {}
        if workerId:
            kwargs.update({"workerid": workerId})
        return self.taskResourceApi.update_task_sync(body, workflowId, taskRefName, status, **kwargs)

    def getQueueSizeForTask(self, taskType: str) -> int:
        queueSizesByTaskType = self.taskResourceApi.size(task_type=[taskType])
        queueSize = queueSizesByTaskType.get(taskType, 0)
        return queueSize

    def addTaskLog(self, taskId: str, logMessage: str):
        self.taskResourceApi.log(logMessage, taskId)

    def getTaskLogs(self, taskId: str) -> List[TaskExecLog]:
        return self.taskResourceApi.get_task_logs(taskId)
