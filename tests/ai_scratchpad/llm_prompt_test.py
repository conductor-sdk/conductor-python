import sys
from typing import Dict

from conductor.client.ai.integrations import AzureOpenAIConfig
from conductor.client.ai.orchestrator import AIConfiguration, AIOrchestrator
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
    ai_config = AIConfiguration('my_azure_open_ai', 'text-davinci-003', '', 'text-embedding-ada-002', 'pineconedb')
    api_config = Configuration(
        authentication_settings=AuthenticationSettings(key_id='0092089d-19ff-4931-b3da-fc093029d0ad',
                                                       key_secret='lzCCrpk5NLi0TYmIDiOfnJWLz5vkxMKn5BoCKIHSddOdYyg3'))

    ai_orchestrator = AIOrchestrator(api_configuration=api_config, ai_configuration=ai_config)
    prompt = Prompt(name='say_hi_to_friend', variables={'friend_name': '${get_friend_name_ref.output.result}'})

    ai_orchestrator.add_ai_integration('my_azure_open_ai', 'azure_openai',
                                       ['text-davinci-003', 'text-embedding-ada-002'], 'viren azure openai',
                                       AzureOpenAIConfig('2dba20b4b1324f078ee00775c4d7733b',
                                                         'https://openai-test-dl.openai.azure.com/'))
    ai_orchestrator.add_prompt_template(prompt.name, 'Hello my ${friend_name}', 'test prompt')
    ai_orchestrator.associate_prompt_template(prompt.name, 'my_azure_open_ai', ['text-davinci-003'])
    result = ai_orchestrator.test_prompt_template('give an evening greeting to ${friend_name}. go: ',
                                                  {'friend_name': 'viren'}, ai_config.llm_provider,
                                                  ai_config.text_complete_model)

    print(result)

    t1 = SimpleTask('get_friend_name', 'get_friend_name_ref')
    t2 = LlmTextComplete('say_hi', 'say_hi_ref', ai_config.llm_provider, ai_config.text_complete_model, prompt=prompt)

    workflow = ConductorWorkflow(executor=ai_orchestrator.workflow_executor, name='say_hi_to_the_friend')
    workflow >> [t1, t2]
    workflow.output_parameters = {'greetings': '${say_hi_ref.output.result}'}
    workflow.execute({}, wait_for_seconds=1)
    print('tokens used: ')
    print(ai_orchestrator.get_token_used_by_model(ai_config.llm_provider, ai_config.text_complete_model))

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
