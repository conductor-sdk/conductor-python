import os
import time
from multiprocessing import set_start_method
from sys import platform

from conductor.client.ai.configuration import LLMProvider
from conductor.client.ai.integrations import OpenAIConfig
from conductor.client.ai.orchestrator import AIOrchestrator
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.llm_tasks.utils.prompt import Prompt

key = os.getenv("KEY")
secret = os.getenv("SECRET")
url = os.getenv("CONDUCTOR_SERVER_URL")
open_ai_key = os.getenv('OPENAI_KEY')


@worker_task(task_definition_name='get_friends_name')
def get_friend_name():
    name = os.getenv('friend')
    if name is None:
        return 'anonymous'
    else:
        return name


def start_workers(api_config):
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
    )
    task_handler.start_processes()
    return task_handler


def main():
    llm_provider = 'open_ai_' + os.getlogin()
    text_complete_model = 'text-davinci-003'
    embedding_complete_model = 'text-embedding-ada-002'

    api_config = Configuration(authentication_settings=AuthenticationSettings(key_id=key, key_secret=secret),
                               server_api_url=url, debug=False)
    task_workers = start_workers(api_config)
    task_workers.join_processes()
    time.sleep(60)

    open_ai_config = OpenAIConfig(open_ai_key)

    kernel = AIOrchestrator(api_configuration=api_config)

    kernel.add_ai_integration(ai_integration_name=llm_provider, provider=LLMProvider.OPEN_AI,
                              models=[text_complete_model, embedding_complete_model],
                              description='openai config',
                              config=open_ai_config)

    # Define and associate prompt with the ai integration
    prompt_name = 'say_hi_to_friend'
    prompt_text = 'give an evening greeting to ${friend_name}. go: '

    kernel.add_prompt_template(prompt_name, prompt_text, 'test prompt')
    kernel.associate_prompt_template(prompt_name, llm_provider, [text_complete_model])

    # Test the prompt
    result = kernel.test_prompt_template('give an evening greeting to ${friend_name}. go: ',
                                         {'friend_name': 'Orkes'}, llm_provider, text_complete_model)

    print(f'test prompt: {result}')

    # Create a 2-step LLM Chain and execute it

    get_name = get_friend_name(task_ref_name='get_friend_name_ref')
    prompt = Prompt(name=prompt_name, variables={'friend_name': get_name.output('result')})

    text_complete = LlmTextComplete('say_hi', 'say_hi_ref', llm_provider, text_complete_model, prompt=prompt)
    text_complete.input('friend_name', get_name.output('result'))

    workflow = ConductorWorkflow(executor=kernel.workflow_executor, name='say_hi_to_the_friend')
    workflow >> get_name >> text_complete

    workflow.output_parameters = {'greetings': text_complete.output('result')}

    # execute the workflow to get the results
    result = workflow()
    print(f'output of the LLM chain workflow: {result.output}')

    # cleanup and stop
    # task_workers.stop_processes()


if __name__ == '__main__':
    # set the no_proxy env
    # see this thread for more context
    # https://stackoverflow.com/questions/55408047/requests-get-not-finishing-doesnt-raise-any-error
    if platform == "darwin":
        os.environ['no_proxy'] = '*'
    set_start_method('fork')
    main()
