from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.worker.worker import Worker
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
from resources.worker.python.python_worker import SimplePythonWorker
from resources.worker.python.python_worker import worker_with_task_result
from time import sleep


WORKFLOW_QUANTITY = 10
WORKFLOW_NAME = 'python_integration_test_workflow'
TASK_NAME = 'python_integration_test_task'


def test_workflow_registration(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = generate_workflow(workflow_executor)
    assert workflow.register(overwrite=True) == None
    return workflow


def test_single_workflow_execution(workflow: ConductorWorkflow, workflow_executor: WorkflowExecutor) -> None:
    workflow_id = workflow_executor.start_workflow(
        start_workflow_request=StartWorkflowRequest(
            name=workflow.name,
        )
    )
    task_handler = TaskHandler(
        configuration=Configuration,
        workers=[
            SimplePythonWorker(
                task_definition_name=TASK_NAME,
            )
        ]
    )
    task_handler.start_processes()
    sleep(5)
    validate_workflow_status(workflow_id)


def test_workflow_execution(workflow: ConductorWorkflow, configuration: Configuration, workflow_executor: WorkflowExecutor) -> None:
    workflow_id_list = workflow_executor.start_workflows(
        quantity=WORKFLOW_QUANTITY,
        workflow_name=workflow.name
    )
    workers = [
        SimplePythonWorker(
            task_definition_name='python_task_example'
        ),
        Worker(
            task_definition_name='python_task_example',
            execute_function=worker_with_task_result,
            poll_interval=0.1,
        )
    ]
    with TaskHandler(workers, configuration) as task_handler:
        task_handler.start_processes()
        sleep(WORKFLOW_QUANTITY * 3)
        for workflow_id in workflow_id_list:
            workflow = workflow_executor.get_workflow(workflow_id, False)


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
    print(
        'checking status of workflow',
        'name:', workflow.workflow_id,
        'workflow_id:', workflow.workflow_id,
        'status:', workflow.status
    )
    assert workflow.status == 'COMPLETED'
