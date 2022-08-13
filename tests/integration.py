import os
from integration.test_workflow_definition import run_workflow_definition_tests
from integration.test_workflow_execution import run_workflow_execution_tests
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import (
    AuthenticationSettings,
)
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor

ENV = {
    'KEY': 'PYTHON_INTEGRATION_TESTS_SERVER_KEY_ID',
    'SECRET': 'PYTHON_INTEGRATION_TESTS_SERVER_KEY_SECRET',
    'URL': 'PYTHON_INTEGRATION_TESTS_SERVER_API_URL',
}


def generate_configuration():
    envs = {}
    for key, env in ENV.items():
        value = os.getenv(env)
        envs[key] = value
    return Configuration(
        server_api_url=envs['URL'],
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id=envs['KEY'],
            key_secret=envs['SECRET'])
        if (envs['KEY'] is not None and envs['SECRET'] is not None)
        else None,
    )


def main():
    configuration = generate_configuration()
    workflow_executor = WorkflowExecutor(configuration)
    run_workflow_definition_tests(workflow_executor)
    run_workflow_execution_tests(configuration, workflow_executor)


if __name__ == "__main__":
    main()
