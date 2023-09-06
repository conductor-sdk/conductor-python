from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.embedding_model import EmbeddingModel
from typing import Any, Dict, List
from typing_extensions import Self


class LlmGenerateEmbeddings(TaskInterface):
    def __init__(self, task_name: str, task_ref_name: str, llm_provider: str, model: str, text: str) -> Self:
        super().__init__(
            task_name=task_name,
            task_reference_name=task_ref_name,
            task_type=TaskType.LLM_GENERATE_EMBEDDINGS,
            input_parameters={
                "llmProvider": llm_provider,
                "model": model,
                "text": text,
            }
        )
