from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import WorkflowRun
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings_workflow import greetings_workflow


def greetings_workflow_run(name: str, workflow_executor: WorkflowExecutor) -> WorkflowRun:
    return workflow_executor.execute(name='hello', version=1, workflow_input={'name': name})


def register_workflow(workflow_executor: WorkflowExecutor):
    workflow = greetings_workflow(workflow_executor=workflow_executor)
    workflow.register(True)


def main():
    # points to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)

    # Needs to be done only when registering a workflow one-time
    register_workflow(workflow_executor)

    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
        import_modules=['greetings']  # import workers from this module
    )
    task_handler.start_processes()

    result = greetings_workflow_run('Orkes', workflow_executor)
    print(f'\nworkflow result: {result.output["result"]}\n')
    task_handler.stop_processes()


if __name__ == '__main__':
    main()
