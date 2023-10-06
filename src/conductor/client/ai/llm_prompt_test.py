import sys
from typing import Dict

from conductor.client.ai.ai_orchestrator import AIConfiguration, AIOrchestrator
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models import Task, TaskResult
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.llm_tasks.utils.prompt import Prompt
from conductor.client.workflow.task.simple_task import SimpleTask


def exec_fn(task: Task) -> TaskResult:
    task_result = TaskResult(
        task_id=task.task_id,
        workflow_instance_id=task.workflow_instance_id,
        worker_id='your_custom_id'
    )
    task_result.add_output_data('worker_style', 'function')
    task_result.add_output_data('name', 'this')
    task_result.status = 'COMPLETED'
    return task_result


def echo(input: Task) -> Dict:
    return 'hello world'


def exec_fn2(task: Task) -> str:
    return 'Hello world222'


def get_document(task: Task) -> str:
    return 'Viren Baraiya'


def main():
    ai_config = AIConfiguration('azure_openai', 'text-davinci-003', 'text-embedding-ada-002', 'pineconedb')
    api_config = Configuration(
        authentication_settings=AuthenticationSettings(key_id='3bbcc893-66f4-4887-a419-12b8117fac62',
                                                       key_secret='t6BhLZUqaKRXLEjzEtnVNnjtO5Ll2C1205SSE1rXg3WrRZ7V'))

    prompt_client = AIOrchestrator(api_configuration=api_config, ai_configuration=ai_config)

    prompt = Prompt(name='say_hi_to_friend', variables={'friend_name': '${get_friend_name_ref.output.result}'})
    tasks = [
        SimpleTask('get_friend_name', 'get_friend_name_ref'),
        LlmTextComplete('say_hi', 'say_hi_ref', ai_config.llm_provider, ai_config.text_complete_model, prompt=prompt)
    ]
    workflow = ConductorWorkflow(name='say_hi_to_the_friend')
    workflow >> tasks
    workflow.output_parameters = {'greetings': '${say_hi_ref.output.result}'}
    task_executors = {'get_friend_name_ref': get_document}
    wf_result = prompt_client.execute_workflow(workflow=workflow, wait_for_seconds=10, task_to_exec=task_executors)
    print(wf_result.output)


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
