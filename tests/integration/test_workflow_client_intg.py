import logging
import os
import unittest

from client.orkes.test_orkes_clients import TestOrkesClients
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes.orkes_workflow_client import OrkesWorkflowClient
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from metadata.test_workflow_definition import run_workflow_definition_tests
from workflow.test_workflow_execution import run_workflow_execution_tests

WORKFLOW_NAME = 'ut_wf'
WORKFLOW_UUID = 'ut_wf_uuid'
TASK_NAME = 'ut_task'
CORRELATION_ID = 'correlation_id'

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


def get_configuration():
    key = os.getenv('KEY')
    secret = os.getenv('SECRET')
    url = os.getenv('CONDUCTOR_SERVER_URL')
    configuration = Configuration(server_api_url=url, authentication_settings=AuthenticationSettings(key, secret))
    configuration.debug = False
    configuration.apply_logging_config()
    logger.info(f'key is {key} - {secret} - {url}')
    return configuration


class TestOrkesWorkflowClientIntg(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = get_configuration()
        cls.workflow_client = OrkesWorkflowClient(cls.config)
        logger.info(f'setting up TestOrkesWorkflowClientIntg with config {cls.config}')
        logger.info('START: integration tests')

    @classmethod
    def tearDownClass(cls):
        logger.info('END: integration tests')

    def test_workflows(self):
        configuration = self.config
        workflow_executor = WorkflowExecutor(configuration)

        # test_async.test_async_method(api_client)
        run_workflow_definition_tests(workflow_executor)
        run_workflow_execution_tests(configuration, workflow_executor)

    def test_orkes_clients(self):
        TestOrkesClients(configuration=self.config).run()


