from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from time import sleep
import integration.test_workflow_definition
import integration.test_workflow_execution
import os

KEY_ID = os.getenv('PYTHON_INTEGRATION_TESTS_SERVER_KEY_ID')
KEY_SECRET = os.getenv('PYTHON_INTEGRATION_TESTS_SERVER_KEY_SECRET')
SERVER_API_URL = os.getenv('PYTHON_INTEGRATION_TESTS_SERVER_API_URL')


def generate_configuration():
    return Configuration(
        server_api_url=SERVER_API_URL,
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id=KEY_ID,
            key_secret=KEY_SECRET,
        )
    )


def run_workflow_definition_tests(workflow_executor: WorkflowExecutor) -> None:
    integration.test_workflow_definition.test_kitchensink_workflow_registration(
        workflow_executor
    )


def run_workflow_execution_tests(configuration: Configuration, workflow_executor: WorkflowExecutor) -> None:
    workflow = integration.test_workflow_execution.test_workflow_registration(
        workflow_executor
    )
    integration.test_workflow_execution.test_single_workflow_execution(
        workflow, configuration, workflow_executor
    )
    integration.test_workflow_execution.test_workflow_execution(
        workflow, configuration, workflow_executor
    )


def main():
    configuration = generate_configuration()
    workflow_executor = WorkflowExecutor(configuration)
    run_workflow_definition_tests(workflow_executor)
    run_workflow_execution_tests(configuration, workflow_executor)


if __name__ == '__main__':
    main()
