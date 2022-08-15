from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import StartWorkflowRequest
from conductor.client.worker.worker import Worker
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from resources.worker.python.python_worker import SimplePythonWorker
from resources.worker.python.python_worker import worker_with_generic_return
from resources.worker.python.python_worker import worker_with_task_result
from time import sleep
from typing import List


WORKFLOW_NAME = 'python_integration_test_workflow'
TASK_NAME = 'python_integration_test_task'


def run_workflow_execution_tests(configuration: Configuration, workflow_executor: WorkflowExecutor):
    test_workflow_registration(
        workflow_executor,
    )
    test_workflow_execution(
        quantity=5,
        workflow_name=WORKFLOW_NAME,
        workers=[
            SimplePythonWorker(TASK_NAME),
            Worker(
                task_definition_name=TASK_NAME,
                execute_function=worker_with_task_result,
                domain='functional_worker_with_task_result'
            ),
            Worker(
                task_definition_name=TASK_NAME,
                execute_function=worker_with_generic_return,
                poll_interval=0.05,
            )
        ],
        configuration=configuration,
        workflow_executor=workflow_executor,
        workflow_completion_timeout=10
    )


def test_workflow_registration(workflow_executor: WorkflowExecutor):
    workflow = generate_workflow(workflow_executor)
    assert workflow.register(overwrite=True) == None


def test_workflow_execution(
    quantity: int,
    workflow_name: str,
    workers: List[WorkerInterface],
    configuration: Configuration,
    workflow_executor: WorkflowExecutor,
    workflow_completion_timeout: float,
) -> None:
    requests = []
    for i in range(quantity):
        requests[i] = StartWorkflowRequest(
        name=workflow_name,
        input={}
    )
    workflow_ids = workflow_executor.start_workflows(requests)
    task_handler = TaskHandler(workers, configuration)
    task_handler.start_processes()
    sleep(workflow_completion_timeout)
    for workflow_id in workflow_ids:
        validate_workflow_status(workflow_id, workflow_executor)
    task_handler.stop_processes()


def generate_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    return ConductorWorkflow(
        executor=workflow_executor,
        name=WORKFLOW_NAME,
        version=12345,
    ).add(
        SimpleTask(
            task_def_name=TASK_NAME,
            task_reference_name=TASK_NAME,
        )
    )


def validate_workflow_status(workflow_id: str, workflow_executor: WorkflowExecutor) -> None:
    workflow = workflow_executor.get_workflow(
        workflow_id=workflow_id,
        include_tasks=False,
    )
    assert workflow.status == 'COMPLETED'
