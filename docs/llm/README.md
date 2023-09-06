### Define LLM based workflow

```python
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.llm_tasks.llm_index_text import LlmIndexText
from conductor.client.workflow.task.llm_tasks.llm_generate_embeddings import LlmGenerateEmbeddings
from conductor.client.workflow.task.embedding_model import EmbeddingModel
from conductor.client.workflow.task.simple_task import SimpleTask
import json

SERVER_API_URL = 'http://localhost:8080/api'
KEY_ID = 'keyId'
KEY_SECRET = 'keySecret'

def main():
    configuration = Configuration(
        server_api_url=SERVER_API_URL,
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id=KEY_ID,
            key_secret=KEY_SECRET
        ),
    )
    workflow_executor = WorkflowExecutor(configuration)
    llm_text_comp = LlmTextComplete("llm_text_complete", "llm_text_complete_ref", "openai", "text-davinci-003", "dogs", 0, 0)
    llm_index_text = LlmIndexText("llm_index_text", "llm_index_text_ref", "pineconedb", "", "test", EmbeddingModel("openai", "text-embedding-ada-002"), "hello world", "hello")
    llm_gen_embeddings = LlmGenerateEmbeddings("llm_generate_embeddings", "llm_generate_embeddings_ref", "openai", "text-davinci-003", "${llm_text_complete_ref.output.result}")
    
    workflow = ConductorWorkflow(executor=workflow_executor,name='llm_text_complete_wf',description='llm workflow',version=1)
    workflow >> llm_text_comp >> llm_index_text >> llm_gen_embeddings

    workflow.register(True)

if __name__ == '__main__':
    main()
```