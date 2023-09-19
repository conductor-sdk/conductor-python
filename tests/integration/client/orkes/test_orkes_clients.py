from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.orkes.metadata_client import MetadataClient
from conductor.client.orkes.models.metadata_tag import MetadataTag

WORKFLOW_NAME = 'IntegrationTestMetadataClientWf'
TASK_TYPE = 'IntegrationTestTask'

class TestOrkesClients:
    def __init__(self, configuration: Configuration):
        self.workflow_executor = WorkflowExecutor(configuration)
        self.metadata_client = MetadataClient(configuration)

    def run(self) -> None:
        self.test_task_definition_lifecycle()
        self.test_workflow_definition_lifecycle()

    def test_task_definition_lifecycle(self):
        taskDef = TaskDef(
            name= TASK_TYPE,
            description="Integration Test Task",
            input_keys=["a", "b"]
        )

        self.__test_register_task_definition(taskDef)
        self.__test_get_task_definition()
        self.__test_update_task_definition(taskDef)
        self.__test_task_tags()
        self.__test_unregister_task_definition()

    def test_workflow_definition_lifecycle(self):
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
        self.__test_workflow_tags()
        self.__test_workflow_rate_limit()
        self.__test_unregister_workflow_definition()
        self.__test_get_invalid_workflow_definition()

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

    def __test_register_workflow_definition(self, workflowDef: WorkflowDef):
        self.metadata_client.registerWorkflowDef(workflowDef, True)

    def __test_get_workflow_definition(self):
        wfDef, _ = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        assert wfDef.name == WORKFLOW_NAME
        assert len(wfDef.tasks) == 1

    def __test_update_workflow_definition(self, workflow: ConductorWorkflow):
        workflow >> SimpleTask("simple_task", "simple_task_ref_2")
        updatedWorkflowDef = workflow.to_workflow_def()
        self.metadata_client.updateWorkflowDef(updatedWorkflowDef, True)
        wfDef, _ = self.metadata_client.getWorkflowDef(WORKFLOW_NAME)
        assert len(wfDef.tasks) == 2

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
        assert(self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME), None)

        self.metadata_client.setWorkflowRateLimit(2, WORKFLOW_NAME)
        assert(self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME), 2)

        self.metadata_client.setWorkflowRateLimit(10, WORKFLOW_NAME)
        assert(self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME), 10)

        self.metadata_client.removeWorkflowRateLimit(WORKFLOW_NAME)
        assert(self.metadata_client.getWorkflowRateLimit(WORKFLOW_NAME), None)
