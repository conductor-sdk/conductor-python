from conductor.client.worker.worker_task import WorkerTask
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.llm_tasks.utils.prompt import Prompt
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.http.models import Task, TaskResult
from conductor.client.ai.ai_orchestrator import AIOrchestrator
from conductor.client.ai.ai_orchestrator import AIConfiguration
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings


@WorkerTask(task_definition_name="get_friend_name")
def getName(task: Task) -> str:
    return 'Steve Jobs'


def main():
    ai_config = AIConfiguration('azure_openai', 'text-davinci-003', 'text-embedding-ada-002', 'pineconedb')
    api_config = Configuration(authentication_settings=AuthenticationSettings(key_id='3bbcc893-66f4-4887-a419-12b8117fac62',key_secret='t6BhLZUqaKRXLEjzEtnVNnjtO5Ll2C1205SSE1rXg3WrRZ7V'))

    prompt_client = AIOrchestrator(api_configuration=api_config, ai_configuration=ai_config)
    prompt_client.add_prompt_template('say_hi_to_friend',
                                      'Say hello to your new friend ${friend_name} based on the time of the day.',
                                      'xxx template')

    #result = prompt_client.test_prompt_template('say_hi_to_friend', {'friend_name': 'viren'})
    #print(result)

    prompt = Prompt(name='say_hi_to_friend', variables={'friend_name': '${get_friend_name_ref.output.result}'})
    workflow = ConductorWorkflow(name='say_hi_to_the_friend')

    workflow >> SimpleTask(task_def_name='get_friend_name', task_reference_name='get_friend_name_ref',execute_fn=getName)
    workflow >> LlmTextComplete('say_hi', 'say_hi_ref', ai_config.llm_provider,ai_config.text_complete_model, prompt=prompt)

    workflow.output_parameters = {'greetings': '${say_hi_ref.output.result}'}

    wf_result = prompt_client.execute_workflow(workflow=workflow, wait_for_seconds=5)
    print(wf_result.output)
    print('Done')


if __name__ == '__main__':
    main()
