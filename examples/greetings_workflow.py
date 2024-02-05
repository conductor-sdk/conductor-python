from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings import greet


def greetings_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    name = 'hello'
    workflow = ConductorWorkflow(name=name, executor=workflow_executor)
    workflow.version = 1
    workflow >> greet(task_ref_name='greet_ref', name=workflow.input('name'))
    return workflow
