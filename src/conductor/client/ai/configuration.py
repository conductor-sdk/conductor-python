from typing import List

from typing_extensions import Self


class AIConfiguration:
    def __init__(self, llm_provider: str, text_complete_model: str, chat_complete_model: str, embedding_model: str,
                 vector_db: str) -> Self:
        self.llm_provider = llm_provider
        self.text_complete_model = text_complete_model
        self.chat_complete_model = chat_complete_model
        self.embedding_model = embedding_model
        self.vector_db = vector_db


