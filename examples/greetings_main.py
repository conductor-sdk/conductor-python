import os
from multiprocessing import set_start_method

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from examples.greetings import greetings_workflow


def main():

    # Key and Secret are required for the servers with authentication enabled.
    key = os.getenv("KEY")
    secret = os.getenv("SECRET")
    url = os.getenv("CONDUCTOR_SERVER_URL")

    api_config = Configuration(authentication_settings=AuthenticationSettings(key_id=key, key_secret=secret),
                               server_api_url=url, debug=False)

    workflow_executor = WorkflowExecutor(configuration=api_config)
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
    )
    task_handler.start_processes()
    result = greetings_workflow('Orkes', workflow_executor)
    print(f'workflow result: {result}')
    task_handler.stop_processes()

if __name__ == '__main__':
    set_start_method('fork')
    main()
