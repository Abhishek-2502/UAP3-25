from typing import List
from pydantic import BaseModel


# Model for the query input (for /generate-embeddings)
class TextModel(BaseModel):
    text: str

# Model for the embedding output (for /generate-embeddings response)
class EmbeddingModel(BaseModel):
    text_embeddings: List[float]
