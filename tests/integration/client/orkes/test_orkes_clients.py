from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.metadata_client import MetadataClient
from conductor.client.orkes.workflow_client import WorkflowClient
from conductor.client.orkes.task_client import TaskClient
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from shortuuid import uuid

WORKFLOW_NAME = 'IntegrationTestOrkesClientsWf_' + str(uuid())
TASK_TYPE = 'IntegrationTestOrkesClientsTask_' + str(uuid())

class TestOrkesClients:
    def __init__(self, configuration: Configuration):
        self.workflow_executor = WorkflowExecutor(configuration)
        self.metadata_client = MetadataClient(configuration)
        self.workflow_client = WorkflowClient(configuration)
        self.task_client = TaskClient(configuration)
        self.workflow_id = None

    def run(self) -> None:
        self.test_workflow_lifecycle()
        self.test_task_lifecycle()

    def test_workflow_lifecycle(self):
        workflow = ConductorWorkflow(
            executor=self.workflow_executor,
            name=WORKFLOW_NAME,
            description='Test Create Workflow',
            version=1
        )
        workflow.input_parameters(["a", "b"])
        workflow >> SimpleTask("simple_task", "simple_task_ref")
        workflowDef = workflow.to_workflow_def()

        self.__test_register_workflow_definition(workflowDef)
        self.__test_get_workflow_definition()
        self.__test_update_workflow_definition(workflow)
        self.__test_workflow_execution_lifecycle()
        self.__test_workflow_tags()
        # self.__test_workflow_rate_limit()
        self.__test_unregister_workflow_definition()
        self.__test_get_invalid_workflow_definition()

    def test_task_lifecycle(self):
        taskDef = TaskDef(
            name= TASK_TYPE,
            description="Integration Test Task",
            input_keys=["a", "b"]
        )

        self.__test_register_task_definition(taskDef)
        self.__test_get_task_definition()
        self.__test_update_task_definition(taskDef)
        self.__test_task_tags()
        self.__test_task_execution_lifecycle()
        self.__test_unregister_task_definition()

    def __test_register_workflow_definition(self, workflowDef: WorkflowDef):
        self.workflow_id = self.metadata_client.registerWorkflowDef(workflowDef, True)

    def __test_get_workflow_definition(self):
        wfDef, _ = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        assert wfDef.name == WORKFLOW_NAME
        assert len(wfDef.tasks) == 1

    def __test_update_workflow_definition(self, workflow: ConductorWorkflow):
        workflow >> SimpleTask("simple_task", "simple_task_ref_2")
        workflow >> SimpleTask("simple_task", "simple_task_ref_3")
        workflow.workflow_id = self.workflow_id
        updatedWorkflowDef = workflow.to_workflow_def()
        self.metadata_client.updateWorkflowDef(updatedWorkflowDef, True)
        wfDef, _ = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        print(len(wfDef.tasks))
        assert len(wfDef.tasks) == 3

    def __test_unregister_workflow_definition(self):
        self.metadata_client.unregisterWorkflowDef(WORKFLOW_NAME, 1)

    def __test_get_invalid_workflow_definition(self):
        wfDef, error = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        assert wfDef == None
        assert error != None

    def __test_task_tags(self):
        tags = [
            MetadataTag("tag1", "val1"),
            MetadataTag("tag2", "val2"),
            MetadataTag("tag3", "val3")
        ]

        self.metadata_client.addTaskTag(tags[0], TASK_TYPE)
        fetchedTags = self.metadata_client.getTaskTags(TASK_TYPE)
        assert len(fetchedTags) == 1
        assert fetchedTags[0].key == tags[0].key

        self.metadata_client.setTaskTags(tags, TASK_TYPE)
        fetchedTags = self.metadata_client.getTaskTags(TASK_TYPE)
        assert len(fetchedTags) == 3

        tagStr = MetadataTag("tag2", "val2")
        self.metadata_client.deleteTaskTag(tagStr, TASK_TYPE)
        assert(len(self.metadata_client.getTaskTags(TASK_TYPE))) == 2

    def __test_workflow_tags(self):
        singleTag = MetadataTag("wftag", "val")

        self.metadata_client.addWorkflowTag(singleTag, WORKFLOW_NAME)
        fetchedTags = self.metadata_client.getWorkflowTags(WORKFLOW_NAME)
        assert len(fetchedTags) == 1
        assert fetchedTags[0].key == singleTag.key

        tags = [
            MetadataTag("wftag", "val"),
            MetadataTag("wftag2", "val2"),
            MetadataTag("wftag3", "val3")
        ]

        self.metadata_client.setWorkflowTags(tags, WORKFLOW_NAME)
        fetchedTags = self.metadata_client.getWorkflowTags(WORKFLOW_NAME)
        assert len(fetchedTags) == 3

        tag = MetadataTag("wftag2", "val2")
        self.metadata_client.deleteWorkflowTag(tag, WORKFLOW_NAME)
        assert(len(self.metadata_client.getWorkflowTags(WORKFLOW_NAME))) == 2

    def __test_workflow_rate_limit(self):
        assert self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME) == None

        self.metadata_client.setWorkflowRateLimit(2, WORKFLOW_NAME)
        assert self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME) == 2

        self.metadata_client.setWorkflowRateLimit(10, WORKFLOW_NAME)
        assert self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME) == 10

        self.metadata_client.removeWorkflowRateLimit(WORKFLOW_NAME)
        assert self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME) == None

    def __test_workflow_execution_lifecycle(self):
        wfInput = { "a" : 5, "b": "+", "c" : [7, 8] }
        workflow_uuid = self.workflow_client.startWorkflowByName(WORKFLOW_NAME, wfInput)
        assert workflow_uuid is not None

        workflow, _ = self.workflow_client.getWorkflow(workflow_uuid, False)
        assert workflow.input["a"] == 5
        assert workflow.input["b"] == "+"
        assert workflow.input["c"] == [7, 8]
        assert workflow.status == "RUNNING"

        self.workflow_client.pauseWorkflow(workflow_uuid)
        workflow, _ = self.workflow_client.getWorkflow(workflow_uuid, False)
        assert workflow.status == "PAUSED"

        self.workflow_client.resumeWorkflow(workflow_uuid)
        workflow, _ = self.workflow_client.getWorkflow(workflow_uuid, False)
        assert workflow.status == "RUNNING"

        self.workflow_client.terminateWorkflow(workflow_uuid, "Integration Test")
        workflow, _ = self.workflow_client.getWorkflow(workflow_uuid, False)
        assert workflow.status == "TERMINATED"

        self.workflow_client.restartWorkflow(workflow_uuid)
        workflow, _ = self.workflow_client.getWorkflow(workflow_uuid, False)
        assert workflow.status == "RUNNING"
        
        self.workflow_client.skipTaskFromWorkflow(workflow_uuid, "simple_task_ref_2")
        workflow, _ = self.workflow_client.getWorkflow(workflow_uuid, False)
        assert workflow.status == "RUNNING"

        self.workflow_client.deleteWorkflow(workflow_uuid)
        workflow, error = self.workflow_client.getWorkflow(workflow_uuid, False)
        assert workflow == None
        assert "Workflow with Id: {} not found.".format(workflow_uuid) in error

    def __test_register_task_definition(self, taskDef: TaskDef):
        self.metadata_client.registerTaskDef(taskDef)

    def __test_get_task_definition(self):
        taskDef = self.metadata_client.getTaskDef(TASK_TYPE)
        assert taskDef.name == TASK_TYPE
        assert len(taskDef.input_keys) == 2

    def __test_update_task_definition(self, taskDef: TaskDef):
        taskDef.description = "Integration Test Task New Description"
        taskDef.input_keys = ["a", "b", "c"]
        self.metadata_client.updateTaskDef(taskDef)
        fetchedTaskDef = self.metadata_client.getTaskDef(taskDef.name)
        assert fetchedTaskDef.description == taskDef.description
        assert len(fetchedTaskDef.input_keys) == 3

    def __test_unregister_task_definition(self):
        self.metadata_client.unregisterTaskDef(TASK_TYPE)

    def __test_task_execution_lifecycle(self):
        
        workflow = ConductorWorkflow(
            executor=self.workflow_executor,
            name=WORKFLOW_NAME + "_task",
            description='Test Task Client Workflow',
            version=1
        )
        workflow.input_parameters(["a", "b"])
        workflow >> SimpleTask(TASK_TYPE, "simple_task_ref")
        workflow >> SimpleTask(TASK_TYPE, "simple_task_ref_2")
        
        startWorkflowRequest = StartWorkflowRequest(
            name=WORKFLOW_NAME + "_task",
            version=1,
            workflow_def=workflow.to_workflow_def(),
            input={ "a" : 15, "b": 3, "op" : "+" }
        )
        
        workflow_uuid = self.workflow_client.startWorkflow(startWorkflowRequest)
        workflow, _ = self.workflow_client.getWorkflow(workflow_uuid, False)
        
        workflow_uuid_2 = self.workflow_client.startWorkflow(startWorkflowRequest)
        
        # First task of each workflow is in the queue
        assert self.task_client.getQueueSizeForTask(TASK_TYPE) == 2
        
        polledTask = self.task_client.pollTask(TASK_TYPE)
        assert polledTask.status == TaskResultStatus.IN_PROGRESS
        
        self.task_client.addTaskLog(polledTask.task_id, "Polled task...")
        
        taskExecLogs = self.task_client.getTaskLogs(polledTask.task_id)
        taskExecLogs[0].log == "Polled task..."
        
        # First task of second workflow is in the queue
        assert self.task_client.getQueueSizeForTask(TASK_TYPE) == 1
        
        taskResult = TaskResult(
            workflow_instance_id=workflow_uuid,
            task_id=polledTask.task_id,
            status=TaskResultStatus.COMPLETED
        )
        
        self.task_client.updateTask(taskResult)
        
        task, _ = self.task_client.getTask(polledTask.task_id)
        assert task.status == TaskResultStatus.COMPLETED
        
        # First task of second workflow and second task of first workflow are in the queue
        assert self.task_client.getQueueSizeForTask(TASK_TYPE) == 2
        
        batchPolledTasks = self.task_client.batchPollTasks(TASK_TYPE)
        assert len(batchPolledTasks) == 1

        polledTask = batchPolledTasks[0]
        # Update first task of second workflow
        self.task_client.updateTaskByRefName(
            workflow_uuid_2,
            polledTask.reference_task_name,
            "COMPLETED",
            "task 2 output"
        )
        
        task, _ = self.task_client.getTask(polledTask.task_id)
        assert task.status == TaskResultStatus.COMPLETED
        
        # Second task of both workflows are in the queue
        assert self.task_client.getQueueSizeForTask(TASK_TYPE) == 2
        
        # Update second task of first workflow
        self.task_client.updateTaskByRefName(
            workflow_uuid_2, "simple_task_ref_2", "COMPLETED", "task 2 output"
        )
        
        # Second task of second workflow is in the queue
        assert self.task_client.getQueueSizeForTask(TASK_TYPE) == 1
        
        polledTask = self.task_client.pollTask(TASK_TYPE)
        assert self.task_client.getQueueSizeForTask(TASK_TYPE) == 0
        
        # Update second task of second workflow
        self.task_client.updateTaskSync(
            workflow_uuid, "simple_task_ref_2", "COMPLETED", "task 1 output"
        )
        
        task, _ = self.task_client.getTask(polledTask.task_id)
        assert task.status == TaskResultStatus.COMPLETED
