from shortuuid import uuid
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.orkes.models.access_type import AccessType
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.orkes.orkes_workflow_client import OrkesWorkflowClient
from conductor.client.orkes.orkes_task_client import OrkesTaskClient
from conductor.client.orkes.orkes_scheduler_client import OrkesSchedulerClient
from conductor.client.orkes.orkes_secret_client import OrkesSecretClient
from conductor.client.orkes.orkes_authorization_client import OrkesAuthorizationClient
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.target_ref import TargetRef, TargetType
from conductor.client.http.models.subject_ref import SubjectRef, SubjectType
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.http.models.save_schedule_request import SaveScheduleRequest
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models.upsert_user_request import UpsertUserRequest
from conductor.client.http.models.upsert_group_request import UpsertGroupRequest
from conductor.client.http.models.create_or_update_application_request import CreateOrUpdateApplicationRequest


SUFFIX = str(uuid())
WORKFLOW_NAME = 'IntegrationTestOrkesClientsWf_' + SUFFIX
TASK_TYPE = 'IntegrationTestOrkesClientsTask_' + SUFFIX
SCHEDULE_NAME = 'IntegrationTestSchedulerClientSch_' + SUFFIX
SECRET_NAME = 'IntegrationTestSecretClientSec_' + SUFFIX
APPLICATION_NAME = 'IntegrationTestAuthClientApp_' + SUFFIX
USER_ID = 'integrationtest_' + SUFFIX[0:5].lower() + "@orkes.io"
GROUP_ID = 'integrationtest_group_' + SUFFIX[0:5].lower()

class TestOrkesClients:
    def __init__(self, configuration: Configuration):
        self.workflow_executor = WorkflowExecutor(configuration)
        self.metadata_client = OrkesMetadataClient(configuration)
        self.workflow_client = OrkesWorkflowClient(configuration)
        self.task_client = OrkesTaskClient(configuration)
        self.scheduler_client = OrkesSchedulerClient(configuration)
        self.secret_client = OrkesSecretClient(configuration)
        self.authorization_client = OrkesAuthorizationClient(configuration)
        self.workflow_id = None

    def run(self) -> None:
        workflow = ConductorWorkflow(
            executor=self.workflow_executor,
            name=WORKFLOW_NAME,
            description='Test Create Workflow',
            version=1
        )
        workflow.input_parameters(["a", "b"])
        workflow >> SimpleTask("simple_task", "simple_task_ref")
        workflowDef = workflow.to_workflow_def()
        
        self.test_workflow_lifecycle(workflowDef, workflow)
        self.test_task_lifecycle()
        self.test_secret_lifecycle()
        self.test_scheduler_lifecycle(workflowDef)
        self.test_application_lifecycle()
        self.test_user_group_permissions_lifecycle(workflowDef)

    def test_workflow_lifecycle(self, workflowDef, workflow):
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

    def test_secret_lifecycle(self):
        self.secret_client.putSecret(SECRET_NAME, "secret_value")
        
        assert self.secret_client.getSecret(SECRET_NAME), "secret_value"
        
        self.secret_client.putSecret(SECRET_NAME + "_2", "secret_value_2")
    
        secret_names = self.secret_client.listAllSecretNames()
        
        assert secret_names, [SECRET_NAME, SECRET_NAME + "_2"]
        
        tags = [
            MetadataTag("sec_tag", "val"), MetadataTag("sec_tag_2", "val2")
        ]
        self.secret_client.setSecretTags(tags, SECRET_NAME)
        fetched_tags = self.secret_client.getSecretTags(SECRET_NAME)
        assert len(fetched_tags) == 2
        
        self.secret_client.deleteSecretTags(tags, SECRET_NAME)
        fetched_tags = self.secret_client.getSecretTags(SECRET_NAME)
        assert len(fetched_tags) == 0
        
        assert self.secret_client.secretExists(SECRET_NAME)
        
        self.secret_client.deleteSecret(SECRET_NAME)
        
        assert self.secret_client.secretExists(SECRET_NAME) == False
        
        self.secret_client.deleteSecret(SECRET_NAME + "_2")
        
        assert self.secret_client.listSecretsThatUserCanGrantAccessTo(), []

    def test_scheduler_lifecycle(self, workflowDef):
        startWorkflowRequest = StartWorkflowRequest(
            name=WORKFLOW_NAME, workflow_def=workflowDef
        )
        saveScheduleRequest = SaveScheduleRequest(
            name=SCHEDULE_NAME,
            start_workflow_request=startWorkflowRequest,
            cron_expression= "0 */5 * ? * *"
        )

        self.scheduler_client.saveSchedule(saveScheduleRequest)

        schedule, _ = self.scheduler_client.getSchedule(SCHEDULE_NAME)
        
        assert schedule['name'] == SCHEDULE_NAME
        
        self.scheduler_client.pauseSchedule(SCHEDULE_NAME)
        
        schedules = self.scheduler_client.getAllSchedules(WORKFLOW_NAME)
        
        assert len(schedules) == 1
        assert schedules[0].name == SCHEDULE_NAME
        
        assert schedules[0].paused == True
        
        self.scheduler_client.resumeSchedule(SCHEDULE_NAME)
        
        schedule, _ = self.scheduler_client.getSchedule(SCHEDULE_NAME)
        assert schedule['paused'] == False
        
        times = self.scheduler_client.getNextFewScheduleExecutionTimes("0 */5 * ? * *", limit=1)
        assert(len(times) == 1)
        
        tags = [
            MetadataTag("sch_tag", "val"), MetadataTag("sch_tag_2", "val2")
        ]
        self.scheduler_client.setSchedulerTags(tags, SCHEDULE_NAME)
        fetched_tags = self.scheduler_client.getSchedulerTags(SCHEDULE_NAME)
        assert len(fetched_tags) == 2
        
        self.scheduler_client.deleteSchedulerTags(tags, SCHEDULE_NAME)
        fetched_tags = self.scheduler_client.getSchedulerTags(SCHEDULE_NAME)
        assert len(fetched_tags) == 0
        
        self.scheduler_client.deleteSchedule(SCHEDULE_NAME)

    def test_application_lifecycle(self):
        req = CreateOrUpdateApplicationRequest(APPLICATION_NAME)
        created_app = self.authorization_client.createApplication(req)
        assert created_app.name == APPLICATION_NAME
        
        application = self.authorization_client.getApplication(created_app.id)
        assert application.id == created_app.id
        
        apps = self.authorization_client.listApplications()
        assert True in [app.id == created_app.id for app in apps]
        
        req.name = APPLICATION_NAME + "_updated"
        app_updated = self.authorization_client.updateApplication(req, created_app.id)
        assert app_updated.name == req.name
        
        self.authorization_client.addRoleToApplicationUser(created_app.id, "USER")
        app_user_id = "app:" + created_app.id
        app_user = self.authorization_client.getUser(app_user_id)
        assert True in [r.name == "USER" for r in app_user.roles]

        self.authorization_client.removeRoleFromApplicationUser(created_app.id, "USER")
        app_user = self.authorization_client.getUser(app_user_id)
        assert True not in [r.name == "USER" for r in app_user.roles]
        
        tags = [MetadataTag("auth_tag", "val"), MetadataTag("auth_tag_2", "val2")]
        self.authorization_client.setApplicationTags(tags, created_app.id)
        fetched_tags = self.authorization_client.getApplicationTags(created_app.id)
        assert len(fetched_tags) == 2
        
        self.authorization_client.deleteApplicationTags(tags, created_app.id)
        fetched_tags = self.authorization_client.getApplicationTags(created_app.id)
        assert len(fetched_tags) == 0
        
        self.authorization_client.deleteApplication(created_app.id)

    def test_user_group_permissions_lifecycle(self, workflowDef):
        req = UpsertUserRequest("Integration User", ["USER"])
        created_user = self.authorization_client.upsertUser(req, USER_ID)
        assert created_user.id == USER_ID

        user = self.authorization_client.getUser(USER_ID)
        assert user.id == USER_ID
        assert user.name == req.name
        
        users = self.authorization_client.listUsers()
        assert [user.id == USER_ID for u in users]
        
        req.name = "Integration " + "Updated"
        updated_user = self.authorization_client.upsertUser(req, USER_ID)
        assert updated_user.name == req.name
        
        # Test Groups
        req = UpsertGroupRequest("Integration Test Group", ["USER"])
        created_group = self.authorization_client.upsertGroup(req, GROUP_ID)
        assert created_group.id == GROUP_ID
        
        group = self.authorization_client.getGroup(GROUP_ID)
        assert group.id == GROUP_ID
        
        groups = self.authorization_client.listGroups()
        assert True in [group.id == GROUP_ID for group in groups]
        
        self.authorization_client.addUserToGroup(GROUP_ID, USER_ID)
        users = self.authorization_client.getUsersInGroup(GROUP_ID)
        assert users[0].id == USER_ID
        
        # Test Granting Permissions
        workflowDef.name = WORKFLOW_NAME + "_permissions"
        self.__create_workflow_definition(workflowDef)
        
        subject = SubjectRef(SubjectType.GROUP, GROUP_ID)
        target = TargetRef(TargetType.WORKFLOW_DEF, WORKFLOW_NAME + "_permissions")
        access = [AccessType.EXECUTE]
        
        self.authorization_client.grantPermissions(subject, target, access)
        perms = self.authorization_client.getPermissions(target)
        assert True in [s == subject for s in perms[AccessType.EXECUTE]]
        
        self.authorization_client.removePermissions(subject, target, access)
        perms = self.authorization_client.getPermissions(target)
        assert True not in [s == subject for s in perms[AccessType.EXECUTE]]
        
        self.authorization_client.removeUserFromGroup(GROUP_ID, USER_ID)
        self.authorization_client.deleteUser(USER_ID)
        self.authorization_client.deleteGroup(GROUP_ID)

    def __test_register_workflow_definition(self, workflowDef: WorkflowDef):
        self.workflow_id = self.__create_workflow_definition(workflowDef)
        assert self.workflow_id != None
    
    def __create_workflow_definition(self, workflowDef):
        return self.metadata_client.registerWorkflowDef(workflowDef, True)

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
        
        batchPolledTasks = self.task_client.batchPollTasks(TASK_TYPE)
        assert len(batchPolledTasks) == 1

        polledTask = batchPolledTasks[0]
        # Update first task of second workflow
        self.task_client.updateTaskByRefName(
            workflow_uuid_2,
            polledTask.reference_task_name,
            "COMPLETED",
            "task 2 op 2nd wf"
        )
        
        # Update second task of first workflow
        self.task_client.updateTaskByRefName(
            workflow_uuid_2, "simple_task_ref_2", "COMPLETED", "task 2 op 1st wf"
        )
        
        # # Second task of second workflow is in the queue
        # assert self.task_client.getQueueSizeForTask(TASK_TYPE) == 1
        polledTask = self.task_client.pollTask(TASK_TYPE)

        # Update second task of second workflow
        self.task_client.updateTaskSync(
            workflow_uuid, "simple_task_ref_2", "COMPLETED", "task 1 op 2nd wf"
        )
        
        assert self.task_client.getQueueSizeForTask(TASK_TYPE) == 0
