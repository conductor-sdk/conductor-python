import json
import os
import random
import string
import time
from typing import List

from conductor.client.ai.configuration import LLMProvider
from conductor.client.ai.integrations import OpenAIConfig
from conductor.client.ai.orchestrator import AIOrchestrator
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import TaskDef, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.http.models.workflow_state_update import WorkflowStateUpdate
from conductor.client.orkes_clients import OrkesClients
from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.do_while_task import LoopTask
from conductor.client.workflow.task.dynamic_task import DynamicTask
from conductor.client.workflow.task.human_task import HumanTask
from conductor.client.workflow.task.llm_tasks.llm_chat_complete import LlmChatComplete, ChatMessage
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.timeout_policy import TimeoutPolicy
from conductor.client.workflow.task.wait_task import WaitTask

from customer import Customer


def start_workers(api_config):
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
    )
    task_handler.start_processes()
    return task_handler


@worker_task(task_definition_name='get_customer_list')
def get_customer_list() -> List[Customer]:
    customers = []
    for i in range(100):
        customer_name = ''.join(random.choices(string.ascii_uppercase +
                                               string.digits, k=5))
        spend = random.randint(a=100000, b=9000000)
        customers.append(
            Customer(id=i, name='Customer ' + customer_name,
                     annual_spend=spend,
                     country='US')
        )
    return customers



@worker_task(task_definition_name='get_top_n')
def get_top_n_customers(n: int, customers: List[Customer]) -> List[Customer]:
    customers.sort(key=lambda x: x.annual_spend, reverse=True)
    end = min(n+1, len(customers))
    return customers[1: end]


@worker_task(task_definition_name='generate_promo_code')
def get_top_n_customers() -> str:
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=5))
    return res


@worker_task(task_definition_name='send_email')
def send_email(customer: list[Customer], promo_code: str) -> str:
    return f'Sent {promo_code} to {len(customer)} customers'


@worker_task(task_definition_name='create_workflow')
def create_workflow(steps: list[str], inputs: dict[str, object]) -> dict:
    executor = OrkesClients().get_workflow_executor()
    workflow = ConductorWorkflow(executor=executor, name='copilot_execution', version=1)

    for step in steps:
        if step == 'review':
            task = HumanTask(task_ref_name='review')
            task.input_parameters.update(inputs[step])
            workflow >> task
        else:
            task = SimpleTask(task_reference_name=step, task_def_name=step)
            task.input_parameters.update(inputs[step])
            workflow >> task

    workflow.register(overwrite=True)
    print(f'\n\n\nRegistered workflow by name {workflow.name}\n')
    return workflow.to_workflow_def().toJSON()


@worker_task(task_definition_name='create_workflow2')
def create_workflow_2(steps: list[str], inputs: dict[str, object]) -> ConductorWorkflow:
    executor = OrkesClients().get_workflow_executor()
    workflow = ConductorWorkflow(executor=executor, name='copilot_execution', version=1)

    i = 0
    prev_task = None
    for step in steps:
        task = SimpleTask(task_reference_name=step, task_def_name=step)
        task.input_parameters.update(inputs[step])
        workflow >> task
        i = i + 1

    print(f'workflow is {workflow.to_workflow_def().toJSON()}')
    workflow_run = workflow.execute(workflow_input={}, wait_for_seconds=10)
    return workflow_run.output


def main():
    llm_provider = 'open_ai_' + os.getlogin()
    chat_complete_model = 'gpt-4'
    api_config = Configuration()
    clients = OrkesClients(configuration=api_config)
    workflow_executor = clients.get_workflow_executor()
    metadata_client = clients.get_metadata_client()
    workflow_client = clients.get_workflow_client()
    task_handler = start_workers(api_config=api_config)

    # register our two tasks
    metadata_client.register_task_def(task_def=TaskDef(name='get_weather'))
    metadata_client.register_task_def(task_def=TaskDef(name='get_price_from_amazon'))

    # Define and associate prompt with the AI integration
    prompt_name = 'chat_function_instructions'
    prompt_text = """
    You are a helpful assistant that can answer questions using tools provided.  
    You have the following tools specified as functions in python:
    1. get_customer_list() ->  Customer (useful to get the list of customers / all the customers / customers)
    2. generate_promo_code() -> str (useful to generate a promocode for the customer)
    3. send_email(customer: Customer, promo_code: str) (useful when sending an email to a customer, promo code is the output of the generate_promo_code function)
    4. get_top_n(n: int, customers: List[Customer]) -> List[Customer]
        (
            useful to get the top N customers based on their spend.
            customers as input can come from the output of get_customer_list function using ${get_customer_list.output.result} 
            reference.
            Needs list of customers as input to get the top N. 
        ).
    5. create_workflow(steps: List[str], inputs: dict[str, dict]) -> dict 
       (Useful to chain the function calls.  
       inputs are: 
        steps: which is the list of python functions to be executed
        inputs: a dictionary with key as the function name and value as the dictionary object that is given as the input
                to the function when calling 
       ).
    6. review(input: str) (useful when you wan a human to review something)
    note, if you have to execute multiple steps, then you MUST use create_workflow function.  
    Do not call a function from another function to chain them.  
    
    When asked a question, you can use one of these functions to answer the question if required.
    
    If you have to call these functions, respond with a python code that will call this function. 
    Make sure, when you have to call a function return in the following valid JSON format that can be parsed directly as a json object:
    {
      "type": "function",
      "function": "ACTUAL_PYTHON_FUNCTION_NAME_TO_CALL_WITHOUT_PARAMETERS"
      "function_parameters": "PARAMETERS FOR THE FUNCTION as a JSON map with key as parameter name and value as parameter value"
    }
    
    Rule: Think about the steps to do this, but your output MUST be the above JSON formatted response.
    
    """
    open_ai_config = OpenAIConfig()

    orchestrator = AIOrchestrator(api_configuration=api_config)
    orchestrator.add_ai_integration(ai_integration_name=llm_provider, provider=LLMProvider.OPEN_AI,
                                    models=[chat_complete_model],
                                    description='openai config',
                                    config=open_ai_config)

    orchestrator.add_prompt_template(prompt_name, prompt_text, 'chat instructions')

    # associate the prompts
    orchestrator.associate_prompt_template(prompt_name, llm_provider, [chat_complete_model])

    wf = ConductorWorkflow(name='my_function_chatbot', version=1, executor=workflow_executor)

    user_input = WaitTask(task_ref_name='get_user_input')

    chat_complete = LlmChatComplete(task_ref_name='chat_complete_ref',
                                    llm_provider=llm_provider, model=chat_complete_model,
                                    instructions_template=prompt_name,
                                    messages=[
                                        ChatMessage(role='user',
                                                    message=user_input.output('query'))
                                    ],
                                    max_tokens=1024)

    function_call = DynamicTask(task_reference_name='fn_call_ref', dynamic_task='SUB_WORKFLOW')
    function_call.input_parameters['steps'] = chat_complete.output('function_parameters.steps')
    function_call.input_parameters['inputs'] = chat_complete.output('function_parameters.inputs')
    function_call.input_parameters['subWorkflowName'] = 'copilot_execution'
    function_call.input_parameters['subWorkflowVersion'] = 1

    sub_workflow = SubWorkflowTask(task_ref_name='execute_workflow', workflow_name='copilot_execution', version=1)

    create = create_workflow(task_ref_name='create_workflow', steps=chat_complete.output('function_parameters.steps'),
                             inputs=chat_complete.output('function_parameters.inputs'))
    call_function = SwitchTask(task_ref_name='to_call_or_not', case_expression=chat_complete.output('function'))
    call_function.switch_case('create_workflow', [create, sub_workflow])

    call_one_fun = DynamicTask(task_reference_name='call_one_fun_ref', dynamic_task=chat_complete.output('function'))
    call_one_fun.input_parameters['inputs'] = chat_complete.output('function_parameters')
    call_one_fun.input_parameters['dynamicTaskInputParam'] = 'inputs'

    call_function.default_case([call_one_fun])

    wf >> user_input >> chat_complete >> call_function

    # let's make sure we don't run it for more than 2 minutes -- avoid runaway loops
    wf.timeout_seconds(120).timeout_policy(timeout_policy=TimeoutPolicy.TIME_OUT_WORKFLOW)
    message = """
    I am a helpful bot that can help with your customer management. 
    
    Here are some examples:
    
    1. Get me the list of top N customers
    2. Get the list of all the customers
    3. Get the list of top N customers and send them a promo code
    """
    print(message)
    workflow_run = wf.execute(wait_until_task_ref=user_input.task_reference_name, wait_for_seconds=120)
    workflow_id = workflow_run.workflow_id
    query = input('>> ')
    input_task = workflow_run.get_task(task_reference_name=user_input.task_reference_name)
    workflow_run = workflow_client.update_state(workflow_id=workflow_id,
                                                update_requesst=WorkflowStateUpdate(
                                                    task_reference_name=user_input.task_reference_name,
                                                    task_result=TaskResult(task_id=input_task.task_id, output_data={
                                                        'query': query
                                                    }, status=TaskResultStatus.COMPLETED)
                                                ),
                                                wait_for_seconds=30)

    print(f'https://pg-qa.orkesconductor.com/execution/{workflow_id}')
    task_handler.stop_processes()
    output = json.dumps(workflow_run.output['result'], indent=3)
    print(f"""
    
    {output}
    
    """)


if __name__ == '__main__':
    main()
