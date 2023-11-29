import time
from typing import Optional, List
from uuid import uuid4

from typing_extensions import Self

from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.prompt_resource_api import PromptResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.api_client import ApiClient
from conductor.client.http.models import Task, TaskResult, StartWorkflowRequest, Workflow
from conductor.client.worker.worker import Worker
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.llm_tasks.utils.prompt import Prompt


class AIConfiguration:
    def __init__(self, llm_provider: str, text_complete_model: str, embedding_model: str, vector_db: str) -> Self:
        self.llm_provider = llm_provider
        self.text_complete_model = text_complete_model
        self.embedding_model = embedding_model
        self.vector_db = vector_db


class AIOrchestrator:
    def __init__(self, api_configuration: Configuration, ai_configuration: AIConfiguration,
                 prompt_test_workflow_name: str = '') -> Self:
        self.ai_configuration = ai_configuration
        api_client = ApiClient(api_configuration)
        self.workflow_executor = WorkflowExecutor(api_configuration)
        self.prompt_resource = PromptResourceApi(api_client)
        self.workflow_resource = WorkflowResourceApi(api_client)
        self.prompt_test_workflow_name = prompt_test_workflow_name
        if self.prompt_test_workflow_name == '':
            self.prompt_test_workflow_name = 'prompt_test_' + str(uuid4())

    def add_prompt_template(self, name: str, template: str, description: str):
        self.prompt_resource.save_message_template(template, description, name)
        return self

    def test_prompt_template(self, name: str, variables: dict,
                             stop_words: Optional[List[str]] = [], max_tokens: Optional[int] = 100,
                             temperature: int = 0,
                             top_p: int = 1):
        prompt = Prompt(name, variables)
        llm_text_complete = LlmTextComplete(
            'prompt_test', 'prompt_test',
            self.ai_configuration.llm_provider, self.ai_configuration.text_complete_model,
            prompt,
            stop_words, max_tokens, temperature, top_p
        )
        name = self.prompt_test_workflow_name
        prompt_test_workflow = ConductorWorkflow(
            executor=self.workflow_executor,
            name=name,
            description='Prompt testing workflow from SDK'
        )
        prompt_test_workflow.add(llm_text_complete)
        output = prompt_test_workflow.execute({})
        if 'result' in output.keys():
            return output['result']
        else:
            return ''

    def __get_pending_tasks(self, workflow: Workflow) -> List[Task]:
        pending = []
        for wf_task in workflow.tasks:
            if wf_task.status == 'SCHEDULED':
                pending.append(wf_task)
        return pending

    def execute_workflow(self, workflow: ConductorWorkflow, task_to_exec: dict[str, object] = None,
                         wait_for_seconds: int = 10) -> dict:
        task_to_exec = task_to_exec or {}
        for task in workflow.tasks:
            task_to_exec[task.task_reference_name] = task.executor

        workflow.executor = self.workflow_executor
        request = StartWorkflowRequest()
        request.workflow_def = workflow.to_workflow_def()
        request.input = {}
        request.name = request.workflow_def.name
        request.version = 1

        workflow_id = workflow.start_workflow(request)
        execution = self.workflow_executor.get_workflow(workflow_id, True)
        count = wait_for_seconds - 1

        while len(task_to_exec) > 0 and count > 0:
            pending = self.__get_pending_tasks(execution)
            if len(pending) == 0:
                break
            for wf_task in pending:
                ref_name = wf_task.reference_task_name
                exec_fn = None
                if ref_name in task_to_exec.keys():
                    exec_fn = task_to_exec.pop(ref_name)
                if exec_fn is not None:
                    worker = Worker(execute_function=exec_fn, task_definition_name=wf_task.task_definition.name)
                    exec_result = worker.execute(wf_task)
                    output = {}

                    if isinstance(exec_result, TaskResult):
                        output = exec_result.output_data
                    else:
                        if isinstance(exec_result, dict):
                            output = exec_result
                        else:
                            output['result'] = exec_result
                    execution = self.workflow_executor.update_task_by_ref_name_sync(task_output=output,
                                                                                    task_reference_name=ref_name,
                                                                                    workflow_id=workflow_id,
                                                                                    status='COMPLETED')

                if execution.status != 'RUNNING':
                    break
                else:
                    time.sleep(1)
                    count = count - 1

        count = wait_for_seconds
        while execution.status == 'RUNNING' and count > 0:
            execution = self.workflow_executor.get_workflow(workflow_id, False)
            time.sleep(1)
            count = count - 1

        return execution