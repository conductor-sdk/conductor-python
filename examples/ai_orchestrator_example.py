import os
import uuid
from multiprocessing import set_start_method

from conductor.client.ai.configuration import LLMProvider
from conductor.client.ai.integrations import AzureOpenAIConfig, OpenAIConfig
from conductor.client.ai.orchestrator import AIOrchestrator
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.worker.worker_task import WorkerTask
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.llm_tasks.utils.prompt import Prompt
from conductor.client.workflow.task.simple_task import SimpleTask

key = os.getenv("KEY")
secret = os.getenv("SECRET")
url = os.getenv("CONDUCTOR_SERVER_URL")

azure_open_ai_key = os.getenv('AZURE_OPENAI_KEY')
azure_open_ai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
open_ai_key = os.getenv('OPENAI_KEY')
open_ai_key = 'xxxx'


def start_workers(api_config):
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
    )
    set_start_method('fork', force=True)
    task_handler.start_processes()
    task_handler.join_processes()
    return task_handler


@WorkerTask(task_definition_name='get_friend_name', poll_interval=0.001)
def get_friend_name(obj: object) -> object:
    print('going to get my friends name')
    return {
        'worker_style': 'function',
        'worker_input': 'Task',
        'worker_output': 'object',
        'task_input': obj,
        'status': 'COMPLETED'
    }


def main():
    llm_provider = 'open_ai_' + str(uuid.uuid4())
    text_complete_model = 'gpt-4'
    embedding_complete_model = 'text-embedding-ada-002'

    api_config = Configuration(authentication_settings=AuthenticationSettings(key_id=key, key_secret=secret),
                               server_api_url=url)
    task_handler = start_workers(api_config)

    azure_open_ai_config = AzureOpenAIConfig(azure_open_ai_key, azure_open_ai_endpoint)
    open_ai_config = OpenAIConfig(open_ai_key)

    kernel = AIOrchestrator(api_configuration=api_config)

    kernel.add_ai_integration(ai_integration_name=llm_provider, provider=LLMProvider.OPEN_AI,
                              models=[text_complete_model, embedding_complete_model],
                              description='openai config',
                              config=open_ai_config)

    # Define and associate prompt with the ai integration
    prompt = Prompt(name='say_hi_to_friend', variables={'friend_name': '${get_friend_name_ref.output.result}'})
    kernel.add_prompt_template(prompt.name, 'Hello my ${friend_name}', 'test prompt')
    kernel.associate_prompt_template(prompt.name, llm_provider, [text_complete_model])

    # Test the prompt
    # result = kernel.test_prompt_template('give an evening greeting to ${friend_name}. go: ',
    #                                      {'friend_name': 'viren'}, llm_provider, text_complete_model)
    #
    # print(result)

    # Create a 2-step LLM Chain and execute it
    t1 = SimpleTask('get_friend_name', 'get_friend_name_ref')
    t2 = LlmTextComplete('say_hi', 'say_hi_ref', llm_provider, text_complete_model, prompt=prompt)

    workflow = ConductorWorkflow(executor=kernel.workflow_executor, name='say_hi_to_the_friend')
    workflow >> [t1, t2]
    workflow.output_parameters = {'greetings': '${say_hi_ref.output.result}'}
    # workflow.execute({}, wait_for_seconds=1)

    print('tokens used:')
    print(kernel.get_token_used(llm_provider))


if __name__ == '__main__':
    main()
