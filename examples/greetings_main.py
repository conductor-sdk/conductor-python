from multiprocessing import set_start_method

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import WorkflowRun
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from examples.greetings_workflow import greetings_workflow


def greetings_workflow_run(name: str, workflow_executor: WorkflowExecutor) -> WorkflowRun:
    return workflow_executor.execute(name='hello', version=1, workflow_input={'name': name})


def main():
    # points to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
        import_modules=['examples.greetings']
    )
    task_handler.start_processes()

    workflow = greetings_workflow(workflow_executor=workflow_executor)
    workflow.register(True)

    result = greetings_workflow_run('Orkes', workflow_executor)
    print(f'workflow result: {result.output["result"]}')
    task_handler.stop_processes()


if __name__ == '__main__':
    set_start_method('fork')
    main()
