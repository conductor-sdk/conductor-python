from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing import Any, Dict, List
from typing_extensions import Self


class LlmSearchIndex(TaskInterface):
    def __init__(self, task_name: str, task_ref_name: str, vector_db: str, namespace: str, index: str, llm_provider: str, model: str, prompt_name: str, query: str) -> Self:
        super().__init__(
            task_name=task_name,
            task_reference_name=task_ref_name,
            task_type=TaskType.LLM_SEARCH_INDEX,
            input_parameters={
                "vectorDB": vector_db,
                "namespace": namespace,
                "index": index,
                "llmProvider": llm_provider,
                "model": model,
                "promptName": prompt_name,
                "query": query
            }
        )
