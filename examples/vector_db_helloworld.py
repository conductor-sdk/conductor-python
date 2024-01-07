import os
import time
from multiprocessing import set_start_method, get_context
from sys import platform

from conductor.client.ai.configuration import LLMProvider, VectorDB
from conductor.client.ai.integrations import OpenAIConfig, PineconeConfig
from conductor.client.ai.orchestrator import AIOrchestrator
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes_clients import OrkesClients
from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.llm_tasks.llm_generate_embeddings import LlmGenerateEmbeddings
from conductor.client.workflow.task.llm_tasks.llm_index_text import LlmIndexText
from conductor.client.workflow.task.llm_tasks.llm_query_embeddings import LlmQueryEmbeddings
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.llm_tasks.utils.embedding_model import EmbeddingModel
from conductor.client.workflow.task.llm_tasks.utils.prompt import Prompt


@worker_task(task_definition_name='get_friends_name')
def get_friend_name():
    name = os.getlogin()
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
    vector_db = 'pinecone_' + os.getlogin()
    llm_provider = 'open_ai_' + os.getlogin()
    embedding_model = 'text-embedding-ada-002'

    api_config = Configuration()
    clients = OrkesClients(configuration=api_config)
    workflow_executor = clients.get_workflow_executor()
    workflow_client = clients.get_workflow_client()
    # task_workers = start_workers(api_config)

    open_ai_config = OpenAIConfig()

    orchestrator = AIOrchestrator(api_configuration=api_config)

    orchestrator.add_vector_store(db_integration_name=vector_db, provider=VectorDB.PINECONE_DB,
                                  indices=['hello_world'],
                                  description='pinecone db',
                                  config=PineconeConfig())

    workflow = ConductorWorkflow(name='test_vector_db', version=1, executor=workflow_executor)
    index_text = LlmIndexText(task_ref_name='index_text_ref', vector_db=vector_db, index='test', namespace='hello',
                              embedding_model=EmbeddingModel(provider=llm_provider, model=embedding_model),
                              text="hello - how are you?", doc_id="hello_1",
                              metadata={
                                  "doctype":"testing only"
                              })
    generate_embeddings = LlmGenerateEmbeddings(task_ref_name='generate_embeddings_ref', llm_provider=llm_provider,
                                                model=embedding_model, text='hi')

    query_index = LlmQueryEmbeddings(task_ref_name='query_vectordb', vector_db=vector_db, index='test',
                                     namespace='hello',
                                     embeddings = generate_embeddings.output('result[0]'))

    workflow >> index_text >> generate_embeddings >> query_index

    workflow_run = workflow.execute(workflow_input={})
    print(f'workflow: {workflow_run}')
    # cleanup and stop
    # task_workers.stop_processes()


if __name__ == '__main__':
    main()
