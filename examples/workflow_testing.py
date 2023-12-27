import os
from multiprocessing import set_start_method
from sys import platform
from uuid import uuid4

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models.workflow_test_request import WorkflowTestRequest
from conductor.client.orkes_clients import OrkesClients
from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.http_task import HttpTask
from conductor.client.workflow.task.javascript_task import JavascriptTask
from conductor.client.workflow.task.json_jq_task import JsonJQTask
from conductor.client.workflow.task.set_variable_task import SetVariableTask
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.terminate_task import TerminateTask, WorkflowStatus
from conductor.client.workflow.task.wait_task import WaitTask


def main():
    api_config = Configuration()
    clients = OrkesClients(configuration=api_config)
    workflow_executor = clients.get_workflow_executor()
    workflow_client = clients.get_workflow_client()

    wf = ConductorWorkflow(name='unit_testing_example', version=1, executor=workflow_executor)
    task1 = SimpleTask(task_def_name='hello', task_reference_name='hello_ref_1')
    task2 = SimpleTask(task_def_name='hello', task_reference_name='hello_ref_2')
    task3 = SimpleTask(task_def_name='hello', task_reference_name='hello_ref_3')

    decision = SwitchTask(task_ref_name='switch_ref', case_expression=task1.output('city'))
    decision.switch_case('NYC', task2)
    decision.default_case(task3)

    wf >> HttpTask(task_ref_name='http', http_input={'uri': 'https://orkes-api-tester.orkesconductor.com/api'})
    wf >> task1 >> decision

    task_ref_to_mock_output = {}

    # task1 has two attempts, first one failed and second succeeded
    task_ref_to_mock_output[task1.task_reference_name] = [{
        'status': 'FAILED',
        'output': {
            'key': 'failed'
        }
    },
        {
            'status': 'COMPLETED',
            'output': {
                'city': 'NYC'
            }
        }
    ]

    task_ref_to_mock_output[task2.task_reference_name] = [
        {
            'status': 'COMPLETED',
            'output': {
                'key': 'task2.output'
            }
        }
    ]

    test_request = WorkflowTestRequest(name=wf.name, version=wf.version,
                                       task_ref_to_mock_output=task_ref_to_mock_output,
                                       workflow_def=wf.to_workflow_def())
    run = workflow_client.test_workflow(test_request=test_request)

    print(f'completed the test run')
    print(f'status: {run.status}')
    assert run.status == 'COMPLETED'

    print(f'first task (HTTP) status: {run.tasks[0].task_type}')
    assert run.tasks[0].task_type == 'HTTP'

    print(f'{run.tasks[1].reference_task_name} status: {run.tasks[1].status} (expected to be FAILED)')
    assert run.tasks[1].status == 'FAILED'

    print(f'{run.tasks[2].reference_task_name} status: {run.tasks[2].status} (expected to be COMPLETED')
    assert run.tasks[2].status == 'COMPLETED'

    print(f'{run.tasks[4].reference_task_name} status: {run.tasks[4].status} (expected to be COMPLETED')
    assert run.tasks[4].status == 'COMPLETED'

    # assert that the task3 was executed
    assert run.tasks[4].reference_task_name == task2.task_reference_name


if __name__ == '__main__':
    main()
