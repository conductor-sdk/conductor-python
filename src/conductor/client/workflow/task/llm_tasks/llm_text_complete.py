from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing import Optional, List
from typing_extensions import Self


class LlmTextComplete(TaskInterface):
    def __init__(self, task_name: str, task_ref_name: str, llm_provider: str, model: str, prompt_name: str, stop_words: Optional[List[str]], max_tokens: Optional[int], temperature: int = 0, top_p: int = 0) -> Self:
        optional_input_params = {}

        if stop_words:
            optional_input_params.update({"stopWords": stop_words})

        if max_tokens:
            optional_input_params.update({"maxTokens": max_tokens})
        
        input_params={
            "llmProvider": llm_provider,
            "model": model,
            "promptName": prompt_name,
            "temperature": temperature,
            "topP": top_p,
        }
        
        input_params.update(optional_input_params)
        
        super().__init__(
            task_name=task_name,
            task_reference_name=task_ref_name,
            task_type=TaskType.LLM_TEXT_COMPLETE,
            input_parameters=input_params
        )
