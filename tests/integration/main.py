from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from metadata.test_workflow_definition import run_workflow_definition_tests
from workflow.test_workflow_execution import run_workflow_execution_tests
from client.orkes.test_orkes_clients import TestOrkesClients
from client.event import test_event_client
from client import test_async

import logging
import os

_logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


def generate_configuration():
    required_envs = {
        'KEY': 'KEY',
        'SECRET': 'SECRET',
        'URL': 'CONDUCTOR_SERVER_URL',
    }
    envs = {}
    for key, env in required_envs.items():
        value = os.getenv(env)
        if value is None or value == '':
            _logger.warning(f'ENV not set - {env}')
        else:
            envs[key] = value
    params = {
        'server_api_url': envs['URL'],
        'debug': True,
    }
    if 'KEY' in envs and 'SECRET' in envs:
        params['authentication_settings'] = AuthenticationSettings(
            key_id=envs['KEY'],
            key_secret=envs['SECRET']
        )
    configuration = Configuration(**params)
    configuration.apply_logging_config()
    return configuration


def main():
    configuration = generate_configuration()
    workflow_executor = WorkflowExecutor(configuration)
    api_client = ApiClient(configuration)
    test_event_client.test_kafka_queue_configuration(api_client)
    test_async.test_async_method(api_client)
    run_workflow_definition_tests(workflow_executor)
    run_workflow_execution_tests(configuration, workflow_executor)
    TestOrkesClients(configuration=configuration).run()


if __name__ == "__main__":
    main()
