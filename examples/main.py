import logging
import os
from multiprocessing import set_start_method
from sys import platform

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes_clients import OrkesClients
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.javascript_task import JavascriptTask
from conductor.client.workflow.task.inline import InlineTask
from examples.workers.task_workers import get_user_info, save_order, OrderInfo, process_task

key = os.getenv("KEY")
secret = os.getenv("SECRET")
url = os.getenv("CONDUCTOR_SERVER_URL")

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


class OrderRequest:

    def __init__(self, user_id: str, order_details: OrderInfo) -> None:
        self.user_id = user_id
        self.order_details = order_details


def start_workers(api_config: Configuration) -> TaskHandler:
    task_handler: TaskHandler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
        import_modules=['examples.workers']  # load all the workers from this module
    )

    # Start polling for the workers
    task_handler.start_processes()
    return task_handler


def create_workflow(workflow_executor: WorkflowExecutor):
    workflow = ConductorWorkflow(name='order_processing', executor=workflow_executor,
                                 description='Process a user order')
    workflow.input_parameters(['user_id', 'order_details'])
    # get user details that contains the address
    workflow >> get_user_info(task_ref_name='get_user_info', user_id='${workflow.input.user_id}')

    # Execute simple javascript to
    script = """
        (function(){ 
            $.order_details.address = []
            $.order_details.address.push($.user_details.addresses[0])
            return $.order_details;
        })();
    """

    # Bindings for the $ variables in the above script
    bindings = {
        'order_details': '${workflow.input.order_details}',
        'user_details': '${get_user_info.output}'
    }
    js = JavascriptTask(task_ref_name='add_address_to_order_details', script=script, bindings=bindings)
    so: OrderInfo = save_order(task_ref_name='save_order',
                               order_details='${add_address_to_order_details.output.result}')
    workflow >> js
    workflow >> so >> process_task(task_ref_name='process_task')
    workflow.output_parameters({'final_price': so.sku_price, 'order_id': so.order_id, 'more': js.result})

    return workflow


def main():
    api_config = Configuration(authentication_settings=AuthenticationSettings(key_id=key, key_secret=secret),
                               server_api_url=url)
    task_handler = start_workers(api_config)
    clients = OrkesClients(configuration=api_config)
    workflow_executor = clients.get_workflow_executor()
    workflow = create_workflow(workflow_executor)

    order_details = OrderInfo(order_id=991, sku_price=12.2, quantity=10, sku='S09494')

    workflow.register(True)

    # Let's run this workflow synchronously and get the output (we wait for 10 second for the workflow to complete)
    workflow_input = OrderRequest(user_id='user_id_1234', order_details=order_details)
    output = workflow.execute(workflow_input=workflow_input, wait_for_seconds=10)

    # workflow.start_workflow()

    logger.info(f'workflow output: {output.status} - {output.output}')
    if not output.is_successful():
        logger.error(f'Workflow execution failed with the error {output.status}')
    task_handler.stop_processes()


if __name__ == '__main__':
    # set the no_proxy env
    # see this thread for more context
    # https://stackoverflow.com/questions/55408047/requests-get-not-finishing-doesnt-raise-any-error
    if platform == "darwin":
        os.environ['no_proxy'] = '*'

    # multiprocessing
    set_start_method("fork")

    main()
