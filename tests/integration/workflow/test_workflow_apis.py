import logging
import os
import sys
import unittest
from multiprocessing import set_start_method
from time import sleep

from conductor.client.http.models.workflow_status import WorkflowStatus

from conductor.client.automator.task_handler import TaskHandler

from conductor.client.http.models.start_workflow_request import StartWorkflowRequest

from conductor.client.orkes_clients import OrkesClients
from conductor.client.worker.worker_task import worker_task
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from configuration import get_configuration

WORKFLOW_NAME = "workflow_e2e_tests"
WORKFLOW_DESCRIPTION = "Python SDK Integration Test"
TASK_NAME = "python_integration_test_task"
WORKFLOW_VERSION = 1234
WORKFLOW_OWNER_EMAIL = "test@test"

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


@worker_task(task_definition_name='step1', poll_interval_millis=500)
def step1(name: str):
    return 'Hello from step 1' + name


@worker_task(task_definition_name='step2', poll_interval_millis=500)
def step2(name: str):
    return 'Hello from step 2 ' + name


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_start_method('fork', force=True)
        if sys.platform == "darwin":
            os.environ['no_proxy'] = '*'

        config = get_configuration()
        clients = OrkesClients(configuration=config)
        cls.workflow_client = clients.get_workflow_client()
        cls.metadata_client = clients.get_metadata_client()
        cls.workflow_executor = clients.get_workflow_executor()
        cls._start_workers(cls, configuration=config)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.task_handler.stop_processes()

    def _start_workers(cls, configuration: Configuration):
        cls.task_handler = TaskHandler(
            workers=[],
            configuration=configuration,
            scan_for_annotated_workers=True,
            import_modules=[]
        )
        cls.task_handler.start_processes()



    def test_workflow_creation(self):
        logger.info("Testing workflow creation")
        test_wf = ConductorWorkflow(name=WORKFLOW_NAME, executor=self.workflow_executor)
        t1 = step1(task_ref_name='step1_ref', name=test_wf.input('name'))
        t2 = step1(task_ref_name='step2_ref', name=t1.output('result'))
        test_wf >> t1 >> t2
        self.metadata_client.register_workflow_def(test_wf.to_workflow_def(), True)
        found = self.metadata_client.get_workflow_def(test_wf.name)
        self.assertTrue(found is not None)
        self.assertEqual(2, len(found.tasks))

    def test_workflow_execution(self):
        logger.info("Testing workflow execution")
        request = StartWorkflowRequest()
        request.name = WORKFLOW_NAME
        request.correlation_id = 'correlation_1'
        request.input = {
            'name': 'orkes'
        }
        request.priority = 3
        id = self.workflow_client.start_workflow(request)
        self.assertIsNotNone(id)

        workflow = self.workflow_client.get_workflow(id, include_tasks=True)
        self.assertIsNotNone(workflow)
        for i in range(10):
            workflow = self.workflow_client.get_workflow(id, include_tasks=True)
            if workflow.status == 'COMPLETED':
                break
            else:
                sleep(1)

        workflow = self.workflow_client.get_workflow(id, include_tasks=True)
        self.assertEqual(workflow.status, 'COMPLETED')