from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.do_while_task import LoopTask
from conductor.client.workflow.task.dynamic_fork_task import DynamicForkTask
from conductor.client.workflow.task.fork_task import ForkTask
from conductor.client.workflow.task.join_task import JoinTask
from conductor.client.workflow.task.json_jq_task import JsonJQTask
from conductor.client.workflow.task.set_variable_task import SetVariableTask
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask, InlineSubWorkflowTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.terminate_task import TerminateTask, WorkflowStatus


def run_workflow_definition_tests(workflow_executor: WorkflowExecutor) -> None:
    test_kitchensink_workflow_registration(workflow_executor)


def test_kitchensink_workflow_registration(workflow_executor: WorkflowExecutor) -> None:
    workflow = generate_workflow(workflow_executor)
    assert workflow.register(True) == None
    workflow_id = workflow_executor.start_workflow(
        start_workflow_request=StartWorkflowRequest(
            name=workflow.name
        )
    )
    assert type(workflow_id) == str


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
        task_ref_name='forked',
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
        pre_fork_task=generate_simple_task(10),
        join_task=JoinTask(
            'join'
        ),
    )


def generate_json_jq_task() -> JsonJQTask:
    return JsonJQTask(
        task_ref_name='jq',
        script='{ key3: (.key1.value1 + .key2.value2) }'
    ).input(
        key='value1', value=['a', 'b'],
    ).input(
        key='value2', value=['d', 'e'],
    )


def generate_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = ConductorWorkflow(
        executor=workflow_executor,
        name='python_workflow_example_from_code',
        description='Python workflow example from code',
        version=1234,
    ).add(
        generate_simple_task(12)
    ).add(
        generate_set_variable_task()
    ).add(
        generate_fork_task(workflow_executor)

    ).add(
        generate_dynamic_fork_task()
    )
    workflow >> generate_sub_workflow_task() >> generate_json_jq_task()
    return workflow
