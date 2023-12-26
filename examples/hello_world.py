import os

from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes_clients import OrkesClients
from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.http_task import HttpTask
from conductor.client.workflow.task.javascript_task import JavascriptTask

key = os.getenv("KEY")
secret = os.getenv("SECRET")
url = os.getenv("CONDUCTOR_SERVER_URL")


def main():
    api_config = Configuration(authentication_settings=AuthenticationSettings(key_id=key, key_secret=secret),
                               server_api_url=url)

    clients = OrkesClients(configuration=api_config)
    workflow_executor = clients.get_workflow_executor()

    wf = ConductorWorkflow(name='hello_world', version=1, executor=workflow_executor)

    say_hello_js = """
    function greetings() {
        return {
            "text": "hello " + $.name
        }
    }
    greetings();
    """

    js = JavascriptTask(task_ref_name='hello_script', script=say_hello_js, bindings={'name': '${workflow.input.name}'})
    http_call = HttpTask(task_ref_name='call_remote_api', http_input={
        'uri': 'https://orkes-api-tester.orkesconductor.com/api'
    })

    wf >> js >> http_call
    wf.output_parameters({
        'greetings': js.output()
    })
    result = wf.execute(workflow_input={'name': 'Orkes'})
    op = result.output
    print(f'Workflow output: {op}')


if __name__ == '__main__':
    main()
