from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.do_while_task import LoopTask
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.sub_workflow_task import InlineSubWorkflowTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.terminate_task import TerminateTask, WorkflowStatus
import os


class Worker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('key', 'A')
        task_result.status = TaskResultStatus.COMPLETED
        return task_result


def main():
    configuration = Configuration(
        server_api_url="https://pg-staging.orkesconductor.com/api",
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id=os.getenv('KEY'),
            key_secret=os.getenv('SECRET'),
        )
    )

    workflow_executor = WorkflowExecutor(configuration)

    simple_workflow = ConductorWorkflow(
        executor=workflow_executor,
        name='python_simple_workflow',
    )
    simple_workflow >> SimpleTask('simple_task', 'simple_task_0')

    sub_workflow_inline = InlineSubWorkflowTask(
        task_ref_name='sub_flow_inline',
        workflow=simple_workflow,
    )

    switch_task = SwitchTask(
        task_ref_name='fact_length',
        case_expression="$.number < 15 ? 'LONG':'LONG'",
        use_javascript=True,
    ).input(
        key='number',
        value='${workflow.input.number}',
    ).switch_case(
        case_name='LONG',
        tasks=[
            SimpleTask(
                'simple_long_switch_case',
                'simple_long_switch_case',
            ),
        ],
    ).default_case(
        tasks=[
            TerminateTask(
                task_ref_name="too_short",
                status=WorkflowStatus.FAILED,
                termination_reason="value too short",
            ),
        ],
    )

    do_while_task = LoopTask(
        task_ref_name="loop_until_success",
        iterations=2,
        tasks=switch_task,
    )

    workflow = ConductorWorkflow(
        executor=workflow_executor,
        name='python_kitchensink_workflow_example_from_code',
        description='Python kitchensink workflow example from code',
        version=4,
    )
    workflow >> sub_workflow_inline >> do_while_task

    response = workflow.register(True)
    print(response)


if __name__ == '__main__':
    main()
