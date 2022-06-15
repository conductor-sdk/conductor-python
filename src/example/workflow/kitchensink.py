from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask
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

    simple_task = SimpleTask(
        'python_task_example_from_code',
        'python_task_example_from_code',
    )

    workflow = ConductorWorkflow(
        workflow_executor,
    ).name(
        "python_workflow_example_from_code",
    ).description(
        "Python workflow example from code",
    ).version(
        1,
    ).add(
        simple_task,
    )

    response = workflow.register(True)
    print(response)


if __name__ == '__main__':
    main()
