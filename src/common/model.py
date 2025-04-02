from typing import List
from loguru import logger
from sentence_transformers import SentenceTransformer


def initialize_model(model_name: str) -> SentenceTransformer:
    """Loads the sentence transformer model."""
    logger.info(f"Loading embedding model: {model_name}")
    return SentenceTransformer(model_name, trust_remote_code=True) # type: ignore


def get_embedding(model, data: str, precision: str = "float32") -> List[float]:
    """Generates an embedding for the given text."""
    return model.encode(data, precision=precision).tolist()