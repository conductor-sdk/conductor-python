from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor


@worker_task(task_definition_name='save_order')
def greet(name: str) -> str:
    return f'Hello my friend {name}'


def greetings_workflow(name: str, workflow_exectuor: WorkflowExecutor) -> dict:
    workflow = ConductorWorkflow(name='hello', executor=workflow_exectuor)
    workflow >> greet(task_ref_name='greet_ref', name=workflow.input('name'))
    run = workflow.execute(workflow_input={'name': name})
    return run.output['result']
