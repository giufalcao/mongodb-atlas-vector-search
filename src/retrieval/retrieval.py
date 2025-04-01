import time
from loguru import logger
from typing import List, Any

from clients.mongodb_atlas import AtlasClient
from configs import conf_env
from utils.utils_model import get_embedding

def get_query_embedding(model, query: str) -> List[float]:
    """Gets the embedding for a given query."""
    if not query:
        logger.warning("Empty query received.")
        return []

    query = query.lower().strip()
    logger.info(f"Query: {query}")
    return get_embedding(model, query)


def perform_vector_search(client: AtlasClient, embedding_vector: List[float]) -> List[dict]:
    """Performs a vector search and returns the results."""
    try:
        logger.info("Performing vector search...")
        results = client.vector_search(
            conf_env.settings.MONGODB_COLLECTION_NAME,
            conf_env.settings.MONGODB_INDEX_NAME,
            conf_env.settings.MONGODB_ATTRIBUTE_NAME,
            embedding_vector,
        )

        if results:
            logger.info(f"Found {len(results)} results.")
            return results
        else:
            logger.warning("No results found during vector search.")
            return []
    except Exception as e:
        logger.error(f"Error performing vector search: {e}")
        return []