from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.do_while_task import LoopTask
from conductor.client.workflow.task.dynamic_fork_task import DynamicForkTask
from conductor.client.workflow.task.fork_task import ForkTask
from conductor.client.workflow.task.set_variable_task import SetVariableTask
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask, InlineSubWorkflowTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.terminate_task import TerminateTask, WorkflowStatus
import os


def generate_configuration():
    return Configuration(
        server_api_url="https://pg-staging.orkesconductor.com/api",
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id=os.getenv('KEY'),
            key_secret=os.getenv('SECRET'),
        )
    )


def generate_simple_task(id: int) -> SimpleTask:
    return SimpleTask(
        task_def_name='python_simple_task_from_code',
        task_reference_name=f'python_simple_task_from_code_{id}'
    )


def generate_sub_workflow_inline_task(workflow_executor: WorkflowExecutor) -> InlineSubWorkflowTask:
    return InlineSubWorkflowTask(
        task_ref_name='python_sub_flow_inline_from_code',
        workflow=ConductorWorkflow(
            executor=workflow_executor,
            name='python_simple_workflow'
        ).add(
            task=generate_simple_task(0)
        )
    )


def generate_switch_task() -> SwitchTask:
    return SwitchTask(
        task_ref_name='fact_length',
        case_expression="$.number < 15 ? 'LONG':'LONG'",
        use_javascript=True,
    ).input(
        key='number',
        value='${workflow.input.number}',
    ).switch_case(
        case_name='LONG',
        tasks=[generate_simple_task(i) for i in range(1, 3)],
    ).default_case(
        tasks=[
            TerminateTask(
                task_ref_name="too_short",
                status=WorkflowStatus.FAILED,
                termination_reason="value too short",
            ),
        ],
    )


def generate_do_while_task() -> LoopTask:
    return LoopTask(
        task_ref_name="loop_until_success",
        iterations=2,
        tasks=generate_switch_task(),
    )


def generate_fork_task(workflow_executor: WorkflowExecutor) -> ForkTask:
    return ForkTask(
        task_ref_name='fork',
        forked_tasks=[
            [
                generate_do_while_task(),
                generate_sub_workflow_inline_task(workflow_executor)
            ],
            [generate_simple_task(i) for i in range(3, 5)]
        ]
    )


def generate_sub_workflow_task() -> SubWorkflowTask:
    return SubWorkflowTask(
        task_ref_name='sub_workflow',
        workflow_name='PopulationMinMax'
    )


def generate_set_variable_task() -> SetVariableTask:
    return SetVariableTask(
        task_ref_name='set_state'
    ).input(
        key='call_made', value=True
    ).input(
        key='number', value='value'
    )


def generate_dynamic_fork_task() -> DynamicForkTask:
    return DynamicForkTask(
        task_ref_name='dynamic_fork',
        pre_fork_task=generate_simple_task(10)
    )


def main():
    configuration = generate_configuration()
    workflow_executor = WorkflowExecutor(configuration)
    workflow = ConductorWorkflow(
        executor=workflow_executor,
        name='python_kitchensink_workflow_example_from_code',
        description='Python kitchensink workflow example from code',
        version=5,
    ).add(
        generate_simple_task(0)
    ).add(
        generate_set_variable_task()
    ).add(
        generate_fork_task(workflow_executor)
    )
    workflow >> generate_sub_workflow_task() >> generate_dynamic_fork_task()
    response = workflow.register(True)
    print(response)


if __name__ == '__main__':
    main()
