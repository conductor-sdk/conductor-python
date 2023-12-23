import sys
from multiprocessing import set_start_method

from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from client.orkes.test_orkes_clients import TestOrkesClients
from workflow.test_workflow_execution import run_workflow_execution_tests
from metadata.test_workflow_definition import run_workflow_definition_tests
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
    configuration.debug = False
    configuration.apply_logging_config()

    return configuration


def main():
    configuration = generate_configuration()
    api_client = ApiClient(configuration)
    workflow_executor = WorkflowExecutor(configuration)

    test_async.test_async_method(api_client)
    run_workflow_definition_tests(workflow_executor)
    run_workflow_execution_tests(configuration, workflow_executor)
    TestOrkesClients(configuration=configuration).run()


if __name__ == "__main__":
    # set the no_proxy env
    # see this thread for more context
    # https://stackoverflow.com/questions/55408047/requests-get-not-finishing-doesnt-raise-any-error
    if sys.platform == "darwin":
        os.environ['no_proxy'] = '*'

    # multiprocessing
    set_start_method("fork")
    main()
