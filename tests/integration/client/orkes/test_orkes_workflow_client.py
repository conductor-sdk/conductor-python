import uuid
import json, os
from time import sleep

from src.conductor.client.configuration.configuration import Configuration
from src.conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from src.conductor.client.orkes_clients import OrkesClients
from src.conductor.client.http.api_client import ApiClient
from src.conductor.client.workflow.executor.workflow_executor import WorkflowExecutor


SUFFIX = str(uuid.uuid4())
WAIT_SIGNAL_WF = 'wait_signal_test'
COMPLEX_PARENT_WF = 'complex_wf_signal_test'
COMPLEX_SUB_WF_1 = 'complex_wf_signal_test_subworkflow_1'
COMPLEX_SUB_WF_2 = 'complex_wf_signal_test_subworkflow_2'

class WorkflowClientTest:
    def __init__(self, configuration: Configuration):
        self.api_client = ApiClient(configuration)
        self.workflow_executor = WorkflowExecutor(configuration)

        orkes_clients = OrkesClients(configuration)
        self.workflow_client = orkes_clients.get_workflow_client()
        self.metadata_client = orkes_clients.get_metadata_client()
        self.workflow_executor = orkes_clients.get_workflow_executor()
        self.task_client = orkes_clients.get_task_client()

    def run(self) -> None:
        # Create and register all test workflows
        self.__register_all_workflow()

        # Run all workflow client tests
        self.__test_execute_workflow_sync()
        self.__test_execute_workflow_durable()
        self.__test_execute_workflow_and_get_blocking_wf()
        self.__test_execute_workflow_and_get_blocking_task()
        # Clean up
        self.__cleanup_test_workflow()

        print("✅ All workflow client tests completed successfully!")

    def register_workflow_from_json(self, wfName: str, overwrite: bool = True) -> str:
        # Get the path to the resources directory relative to the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        json_path = os.path.join(project_root, "integration", "resources", wfName+".json")

        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Workflow definition file not found: {json_path}")

        with open(json_path, 'r') as f:
            workflow_json = json.load(f)

        # Convert JSON to WorkflowDef object
        workflow_def = self.api_client.deserialize_class(workflow_json, "WorkflowDef")

        # Register the workflow
        self.metadata_client.register_workflow_def(workflow_def, overwrite)

        print(f"Registered workflow '{workflow_def.name}' (version {workflow_def.version}) from JSON file")
        return workflow_def.name

    def __register_all_workflow(self):
        self.register_workflow_from_json(WAIT_SIGNAL_WF)
        self.register_workflow_from_json(COMPLEX_PARENT_WF)
        self.register_workflow_from_json(COMPLEX_SUB_WF_1)
        self.register_workflow_from_json(COMPLEX_SUB_WF_2)
        print(f"All WFs have been registered")

    def __test_execute_workflow_sync(self):
        start_request = StartWorkflowRequest(
            name=WAIT_SIGNAL_WF,
            version=1,
            input={"param1": "test_value", "param2": 123}
        )

        # Test with SYNCHRONOUS consistency
        workflow_run = self.workflow_client.execute_workflow(
            start_workflow_request=start_request,
            request_id=None,  # Optional unique ID
            wait_until_task_ref=None,
            consistency="SYNCHRONOUS",
            wait_for_seconds=1
        )
        assert workflow_run is not None, "Should return a response"
        assert workflow_run.workflow_id is not None, "Workflow ID should not be None"
        assert workflow_run.status == "RUNNING", "Workflow should be running"
        print(f"✅ execute_workflow test passed")

        self.task_client.signal_workflow_task_a_sync(
            workflow_run.workflow_id,
            output={"result": "success"},
            status="COMPLETED"
        )
        print(f"Workflow task signaled successfully")

        sleep(2)
        workflow = self.workflow_client.get_workflow(workflow_run.workflow_id, include_tasks=True)
        assert workflow.status == "COMPLETED", "Workflow should be completed"

    def __test_execute_workflow_durable(self):
        start_request = StartWorkflowRequest(
            name=WAIT_SIGNAL_WF,
            version=1,
            input={"param1": "test_value", "param2": 123}
        )

        # Test with SYNCHRONOUS consistency
        workflow_run = self.workflow_client.execute_workflow(
            start_workflow_request=start_request,
            request_id=None,  # Optional unique ID
            wait_until_task_ref=None,
            consistency="DURABLE",
            wait_for_seconds=1
        )
        assert workflow_run is not None, "Should return a response"
        assert workflow_run.workflow_id is not None, "Workflow ID should not be None"
        assert workflow_run.status == "RUNNING", "Workflow should be running"
        print(f"✅ execute_workflow test passed")

        self.task_client.signal_workflow_task_a_sync(
            workflow_run.workflow_id,
            output={"result": "success"},
            status="COMPLETED"
        )
        print(f"Workflow task signaled successfully")

        sleep(2)
        workflow = self.workflow_client.get_workflow(workflow_run.workflow_id, include_tasks=True)
        assert workflow.status == "COMPLETED", "Workflow should be completed"


    def __test_execute_workflow_and_get_blocking_wf(self):
        start_request = StartWorkflowRequest(
            name=COMPLEX_PARENT_WF,
            version=1,
            input={"param1": "test_value", "param2": 123}
        )

        # Test with SYNCHRONOUS consistency
        workflow_run = self.workflow_client.execute_workflow_with_blocking_workflow(
            start_workflow_request=start_request,
            request_id=None,  # Optional unique ID
            wait_until_task_ref=None,
            consistency="SYNCHRONOUS",
            wait_for_seconds=1
        )
        assert workflow_run is not None, "Should return a response"
        assert workflow_run.workflow_id is not None, "Workflow ID should not be None"
        assert workflow_run.status == "RUNNING", "Workflow should be running"
        print(f"✅ Workflow executed successfully")

        wfRun = self.task_client.signal_workflow_task_with_blocking_workflow(
            workflow_run.workflow_id,
            output={"result": "success"},
            status="COMPLETED"
        )
        print(f"✅ Signaled WF Task successfully")
        assert wfRun is not None, "Should return a response"
        assert wfRun.status == "RUNNING", "Task should be running"
        sleep(2)

        wfRun = self.task_client.signal_workflow_task_with_blocking_workflow(
            workflow_run.workflow_id,
            output={"result": "success"},
            status="COMPLETED"
        )
        print(f"✅ Signaled WF Task successfully")
        assert wfRun is not None, "Should return a response"
        assert wfRun.status == "RUNNING", "Task should be running"
        sleep(2)

        workflow = self.workflow_client.get_workflow(workflow_run.workflow_id, include_tasks=True)
        assert workflow.status == "COMPLETED", "Workflow should be completed"

    def __test_execute_workflow_and_get_blocking_task(self):
        start_request = StartWorkflowRequest(
            name=COMPLEX_PARENT_WF,
            version=1,
            input={"param1": "test_value", "param2": 123}
        )

        # Test with SYNCHRONOUS consistency
        task_run = self.workflow_client.execute_workflow_with_blocking_task(
            start_workflow_request=start_request,
            request_id=None,  # Optional unique ID
            wait_until_task_ref=None,
            consistency="SYNCHRONOUS",
            wait_for_seconds=1
        )
        assert task_run is not None, "Should return a response"
        assert task_run.workflow_id is not None, "Workflow ID should not be None"
        assert task_run.status == "RUNNING", "Workflow should be running"
        print(f"✅ Workflow executed successfully")

        taskRun = self.task_client.signal_workflow_task_with_blocking_task(
            task_run.workflow_id,
            output={"result": "success"},
            status="COMPLETED"
        )
        print(f"✅ Signaled WF Task successfully")
        assert taskRun is not None, "Should return a response"
        assert taskRun.status == "RUNNING", "Task should be running"
        sleep(2)

        taskRun = self.task_client.signal_workflow_task_with_blocking_task(
            task_run.workflow_id,
            output={"result": "success"},
            status="COMPLETED"
        )
        print(f"✅ Signaled WF Task successfully")
        assert taskRun is not None, "Should return a response"
        assert taskRun.status == "RUNNING", "Task should be running"
        sleep(2)

        workflow = self.workflow_client.get_workflow(task_run.workflow_id, include_tasks=True)
        assert workflow.status == "COMPLETED", "Workflow should be completed"


    # def __test_execute_workflow_with_target_workflow(self):
    #     start_request = StartWorkflowRequest(
    #         name=TEST_WF_NAME,
    #         version=1,
    #         input={"param1": "test_value", "param2": 123}
    #     )
    #
    #     # Test TARGET_WORKFLOW strategy
    #     workflow_run = self.workflow_client.execute_workflow_with_target_workflow(
    #         start_workflow_request=start_request,
    #         request_id=None,  # Optional unique ID
    #         wait_until_task_ref="simple_task_ref",
    #         consistency="SYNCHRONOUS",
    #         wait_for_seconds=5
    #     )
    #     assert workflow_run is not None, "Should return a response"
    #     assert workflow_run.workflow_id is not None, "Workflow ID should not be None"
    #     assert workflow_run.status == "COMPLETED", "Workflow should be completed"
    #     print(f"✅ execute_workflow test passed")

    def __cleanup_test_workflow(self):
        self.metadata_client.unregister_workflow_def(WAIT_SIGNAL_WF, 1)
        self.metadata_client.unregister_workflow_def(COMPLEX_PARENT_WF, 1)
        self.metadata_client.unregister_workflow_def(COMPLEX_SUB_WF_1, 1)
        self.metadata_client.unregister_workflow_def(COMPLEX_SUB_WF_2, 1)
        print(f"✅All Test workflows unregistered")

if __name__ == "__main__":

    api_config = Configuration()
    print(f"Using Conductor server: {api_config.host}")

    # Create and run the test
    test = WorkflowClientTest(api_config)
    test.run()

    print("Test execution complete!")