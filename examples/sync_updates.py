from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import StartWorkflowRequest, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.http.models.workflow_state_update import WorkflowStateUpdate
from conductor.client.orkes_clients import OrkesClients
from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.http_task import HttpTask
from conductor.client.workflow.task.javascript_task import JavascriptTask
from conductor.client.workflow.task.json_jq_task import JsonJQTask
from conductor.client.workflow.task.set_variable_task import SetVariableTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.terminate_task import TerminateTask, WorkflowStatus
from conductor.client.workflow.task.wait_task import WaitTask


def main():
    api_config = Configuration()

    clients = OrkesClients(configuration=api_config)
    workflow_client = clients.get_workflow_client()

    request = StartWorkflowRequest()
    request.name = 'sync_task_variable_updates'
    request.version = 1
    workflow_run = workflow_client.execute_workflow(start_workflow_request=request, wait_for_seconds=10,
                                                    wait_until_task_ref='wait_task_ref')
    print(f'started {workflow_run.workflow_id}')

    task_result = TaskResult()
    task_result.status = TaskResultStatus.COMPLETED

    state_update = WorkflowStateUpdate()
    state_update.task_reference_name = 'wait_task_ref'
    state_update.task_result = task_result
    state_update.variables = {
        'case': 'case1'
    }

    workflow_run = workflow_client.update_state(workflow_id=workflow_run.workflow_id, update_requesst=state_update,
                                                wait_for_seconds=1,
                                                wait_until_task_ref_names=['wait_task_ref_1', 'wait_task_ref_2'])
    last_task_ref = workflow_run.tasks[len(workflow_run.tasks) - 1].reference_task_name
    print(f'workflow: {workflow_run.status}, last task = {last_task_ref}')

    state_update.task_reference_name = last_task_ref
    workflow_run = workflow_client.update_state(workflow_id=workflow_run.workflow_id, update_requesst=state_update,
                                                wait_for_seconds=1)
    print(f'workflow: {workflow_run.status}, last task = {last_task_ref}')


if __name__ == '__main__':
    main()
