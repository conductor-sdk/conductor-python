from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.embedding_model import EmbeddingModel
from typing_extensions import Self


class LlmIndexText(TaskInterface):
    def __init__(self, task_name: str, task_ref_name: str, vector_db: str, namespace: str, index: str, embedding_model: EmbeddingModel, text: str, doc_id: str) -> Self:
        super().__init__(
            task_name=task_name,
            task_reference_name=task_ref_name,
            task_type=TaskType.LLM_INDEX_TEXT,
            input_parameters={
                "vectorDB": vector_db,
                "namespace": namespace,
                "index": index,
                "embeddingModelProvider": embedding_model.provider,
                "embeddingModel": embedding_model.model,
                "text": text,
                "docId": doc_id
            }
        )
