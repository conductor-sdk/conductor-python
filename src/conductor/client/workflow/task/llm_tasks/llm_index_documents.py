from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing import Optional
from conductor.client.workflow.task.embedding_model import EmbeddingModel
from typing_extensions import Self


class LlmIndexDocuments(TaskInterface):
    def __init__(self, task_name: str, task_ref_name: str, vector_db: str, namespace: str, embedding_model: EmbeddingModel, index: str, url: str, media_type: str, chunk_size: Optional[int] = None, chunk_overlap: Optional[int]= None) -> Self:
        input_params = {
            "vectorDB": vector_db,
            "namespace": namespace,
            "index": index,
            "embeddingModelProvider": embedding_model.provider,
            "embeddingModel": embedding_model.model,
            "url": url,
            "mediaType": media_type
        }
        
        optional_input_params = {}
        
        if chunk_size:
            optional_input_params.update({"chunkSize": chunk_size})
        
        if chunk_overlap:
            optional_input_params.update({"chunkOverlap": chunk_overlap})
            
        input_params.update(optional_input_params)
        
        super().__init__(
            task_name=task_name,
            task_reference_name=task_ref_name,
            task_type=TaskType.LLM_INDEX_DOCUMENT,
            input_parameters=input_params
        )
