import os
import time
import uuid
from multiprocessing import set_start_method, Process
from sys import platform
from conductor.client.ai.configuration import LLMProvider
from conductor.client.ai.integrations import AzureOpenAIConfig, OpenAIConfig
from conductor.client.ai.orchestrator import AIOrchestrator
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models import TaskResult, Task
from conductor.client.worker.worker import Worker
from conductor.client.worker.worker_task import WorkerTask
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.llm_tasks.utils.prompt import Prompt
from conductor.client.workflow.task.simple_task import SimpleTask

key = os.getenv("KEY")
secret = os.getenv("SECRET")
url = os.getenv("CONDUCTOR_SERVER_URL")
open_ai_key = os.getenv('OPENAI_KEY')


def start_workers(api_config):
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
    )
    task_handler.start_processes()
    return task_handler


def main():
    llm_provider = 'open_ai_' + str(uuid.uuid4())
    text_complete_model = 'gpt-4'
    embedding_complete_model = 'text-embedding-ada-002'

    api_config = Configuration(authentication_settings=AuthenticationSettings(key_id=key, key_secret=secret),
                               server_api_url=url, debug=False)
    start_workers(api_config)

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
    result = kernel.test_prompt_template('give an evening greeting to ${friend_name}. go: ',
                                         {'friend_name': 'viren'}, llm_provider, text_complete_model)

    print(result)

    # Create a 2-step LLM Chain and execute it
    t1 = SimpleTask('get_friend_name', 'get_friend_name_ref')
    # enable caching
    t2 = LlmTextComplete('say_hi', 'say_hi_ref', llm_provider, text_complete_model, prompt=prompt)

    workflow = ConductorWorkflow(executor=kernel.workflow_executor, name='say_hi_to_the_friend')
    workflow >> [t1, t2]
    workflow.output_parameters = {'greetings': '${say_hi_ref.output.result}'}
    workflow.execute({}, wait_for_seconds=1)

    print('tokens used:')
    print(kernel.get_token_used(llm_provider))


def task():
    while True:
        print('Hello from new process', flush=True)
        time.sleep(1)


if __name__ == '__main__':
    if platform == "darwin":
        os.environ['no_proxy'] = '*'
    set_start_method('fork')
    main()
