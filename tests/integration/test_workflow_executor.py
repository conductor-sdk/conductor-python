from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.worker.worker import Worker
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from resources.worker.python.python_worker import SimplePythonWorker, execute
from time import sleep
from typing import List

workflow_quantity = 15


def test_workflow_execution(configuration: Configuration, workflow_executor: WorkflowExecutor) -> None:
    workflow = generate_workflow(workflow_executor)
    assert workflow.register(overwrite=True) == None
    workflow_id_list = start_workflows(
        workflow_quantity,
        workflow,
        workflow_executor
    )
    workers = [
        SimplePythonWorker(
            task_definition_name='python_task_example'
        ),
        Worker(
            task_definition_name='python_task_example',
            execute_function=execute,
            poll_interval=0.25,
        )
    ]
    with TaskHandler(workers, configuration) as task_handler:
        task_handler.start_processes()
        sleep(workflow_quantity)
        for workflow_id in workflow_id_list:
            workflow = workflow_executor.get_workflow(workflow_id, False)
            assert workflow.status == 'COMPLETED'


def generate_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    return ConductorWorkflow(
        executor=workflow_executor,
        name='python_workflow_example_from_code',
        description='Python workflow example from code',
        version=1234,
    ).add(
        SimpleTask(
            task_def_name='python_task_example',
            task_reference_name='python_task_example'
        )
    )


def start_workflows(qty: int, workflow: ConductorWorkflow, workflow_executor: WorkflowExecutor) -> List[str]:
    workflow_id_list = []
    for _ in range(qty):
        workflow_id = workflow_executor.start_workflow(
            start_workflow_request=StartWorkflowRequest(
                name=workflow.name
            )
        )
        workflow_id_list.append(workflow_id)
    return workflow_id_list
