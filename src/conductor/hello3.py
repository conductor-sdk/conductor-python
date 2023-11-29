import functools
from typing import List

from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.worker.worker_task import WorkerTask
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.task import TaskInterface
from conductor.hello import workflow


@WorkerTask(task_definition_name="get_user_info")
def get_user_info():
    pass


@WorkerTask(task_definition_name="send_email")
def send_email():
    pass


@WorkerTask(task_definition_name="send_sms")
def send_sms():
    pass


def RunsOn(cpu, memory):
    pass


@WorkerTask(task_definition_name="record_notification")
@RunsOn(cpu=2, memory='1Mi')
def record_notification():
    pass


@WorkerTask(task_definition_name="capture_audit")
def capture_audit():
    pass


@workflow(name='user_notification', schedule='0 0 * ? * *')
def user_notification_workflow() -> List[TaskInterface]:
    switch = SwitchTask('email_or_sms_ref', '${get_user_info.output.preference}')
    switch = switch.switch_case('email', send_email)
    switch = switch.switch_case('sms', send_sms)
    return get_user_info >> switch >> record_notification


def assistant(func):
    pass


@assistant
def get_movie_recommendation(prompt: str):
    pass


def main():
    executor = WorkflowExecutor(
        configuration=Configuration(authentication_settings=AuthenticationSettings(key_id='', key_secret='')))
    workflow = ConductorWorkflow(name='user_notification', executor=executor)
    email_or_sms = SwitchTask('email_or_sms_ref', '${get_user_info.output.preference}')
    email_or_sms = email_or_sms.switch_case('email', send_email)
    email_or_sms = email_or_sms.switch_case('sms', send_sms)
    workflow >> get_user_info >> email_or_sms >> [record_notification, capture_audit]

    output = workflow.execute({'username': 'user1@ores.io'})
    print(output)

    workflow.schedule('0 0 * ? * *', {'username': 'user1@ores.io'})
    pass


if __name__ == '__main__':
    main()
