from enum import Enum


class LLMProvider(str, Enum):
    AZURE_OPEN_AI = "azure_openai",
    OPEN_AI = "openai"
    GCP_VERTEX_AI = "vertex_ai",
    HUGGING_FACE = "huggingface"


class VectorDB(str, Enum):
    PINECONE_DB = "pineconedb",
    WEAVIATE_DB = "weaviatedb"
