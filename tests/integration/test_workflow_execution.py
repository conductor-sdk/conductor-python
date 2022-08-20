from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.worker import ExecuteTaskFunction
from conductor.client.http.models import StartWorkflowRequest
from conductor.client.worker.worker import Worker
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from resources.worker.python.python_worker import ClassWorker
from resources.worker.python.python_worker import ClassWorkerWithDomain
from resources.worker.python.python_worker import worker_with_generic_input_and_generic_output
from resources.worker.python.python_worker import worker_with_generic_input_and_task_result_output
from resources.worker.python.python_worker import worker_with_task_input_and_generic_output
from resources.worker.python.python_worker import worker_with_task_input_and_task_result_output
from time import sleep
from typing import List
import resources.workflow.properties as test_properties


def run_workflow_execution_tests(configuration: Configuration, workflow_executor: WorkflowExecutor):
    test_workflow_registration(
        workflow_executor,
    )
    test_workflow_execution(
        workflow_quantity=15,
        workflow_name=test_properties.WORKFLOW_NAME,
        workers=[
            ClassWorker(test_properties.TASK_NAME),
            ClassWorkerWithDomain(test_properties.TASK_NAME),
            generate_worker(worker_with_generic_input_and_generic_output),
            generate_worker(worker_with_generic_input_and_task_result_output),
            generate_worker(worker_with_task_input_and_generic_output),
            generate_worker(worker_with_task_input_and_task_result_output),
        ],
        configuration=configuration,
        workflow_executor=workflow_executor,
        workflow_completion_timeout=15
    )


def test_workflow_registration(workflow_executor: WorkflowExecutor):
    workflow = generate_workflow(workflow_executor)
    assert workflow.register(overwrite=True) == None


def test_workflow_execution(
    workflow_quantity: int,
    workflow_name: str,
    workers: List[WorkerInterface],
    configuration: Configuration,
    workflow_executor: WorkflowExecutor,
    workflow_completion_timeout: float,
) -> None:
    start_workflow_requests = [None] * workflow_quantity
    for i in range(workflow_quantity):
        start_workflow_requests[i] = StartWorkflowRequest(name=workflow_name)
    workflow_ids = workflow_executor.start_workflows(start_workflow_requests)
    task_handler = TaskHandler(workers, configuration)
    task_handler.start_processes()
    sleep(workflow_completion_timeout)
    for workflow_id in workflow_ids:
        validate_workflow_status(workflow_id, workflow_executor)
    task_handler.stop_processes()


def generate_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    return ConductorWorkflow(
        executor=workflow_executor,
        name=test_properties.WORKFLOW_NAME,
        version=12345,
    ).add(
        SimpleTask(
            task_def_name=test_properties.TASK_NAME,
            task_reference_name=test_properties.TASK_NAME,
        )
    )


def validate_workflow_status(workflow_id: str, workflow_executor: WorkflowExecutor) -> None:
    workflow = workflow_executor.get_workflow(
        workflow_id=workflow_id,
        include_tasks=False,
    )
    assert workflow.status == 'COMPLETED'


def generate_worker(execute_function: ExecuteTaskFunction) -> Worker:
    return Worker(
        task_definition_name=test_properties.TASK_NAME,
        execute_function=execute_function,
        poll_interval=0.05
    )
