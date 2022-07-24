from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker import Worker
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from time import sleep
from typing import List
import os


class SimplePythonWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('worker_style', 'class')
        task_result.add_output_data('secret_number', 1234)
        task_result.add_output_data('is_it_true', False)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 500ms
        return 0.5


def execute(task: Task) -> TaskResult:
    task_result = TaskResult(
        task_id=task.task_id,
        workflow_instance_id=task.workflow_instance_id,
        worker_id='your_custom_id'
    )
    task_result.add_output_data('worker_style', 'function')
    task_result.status = TaskResultStatus.COMPLETED
    return task_result


def get_configuration() -> Configuration:
    return Configuration(
        server_api_url="https://pg-staging.orkesconductor.com/api",
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id=os.getenv('KEY'),
            key_secret=os.getenv('SECRET'),
        )
    )


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


def test_workflow_execution(configuration: Configuration, workflow_executor: WorkflowExecutor) -> None:
    workflow = generate_workflow(workflow_executor)
    assert workflow.register(overwrite=True) == None
    workflow_id_list = start_workflows(5, workflow, workflow_executor)
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
        sleep()

        task_handler.join_processes()
