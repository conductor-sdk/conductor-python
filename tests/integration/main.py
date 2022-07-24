from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from test_workflow_definition import test_kitchensink_workflow_registration
import os


def generate_configuration():
    return Configuration(
        server_api_url="https://pg-staging.orkesconductor.com/api",
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id=os.getenv('KE'),
            key_secret=os.getenv('SECRET'),
        )
    )


def main():
    configuration = generate_configuration()
    workflow_executor = WorkflowExecutor(configuration)
    test_kitchensink_workflow_registration(workflow_executor)
    print('passed kitchensink workflow registration')


if __name__ == '__main__':
    main()
