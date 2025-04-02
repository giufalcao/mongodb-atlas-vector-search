from typing import List
from loguru import logger
from sentence_transformers import SentenceTransformer

from src.clients.mongodb_atlas import AtlasClient
from src.common.model import get_embedding, initialize_model


def generate_query_embedding(model: SentenceTransformer, query_text: str):
    """Generates an embedding for the query text."""
    logger.info(f"Generating embedding for query: '{query_text}'")
    return get_embedding(model, query_text)


def run_vector_search(client: AtlasClient, index_name: str, embed_field: str, embedding: List[float]):
    """Runs a vector search on MongoDB Atlas and returns the results."""
    logger.info("Performing vector search in MongoDB Atlas.")
    results = client.run_vector_search_index(index_name, embed_field, embedding)

    if results:
        logger.info(f"Vector search returned {len(results)} results.")
    else:
        logger.warning("No relevant documents found.")

    return results


def log_search_results(results):
    """Logs the retrieved search results."""
    if results:
        for doc in results:
            logger.info(
                f"Movie ID: {doc['_id']} | Title: {doc['title']} | "
                f"Year: {doc['year']} | Search Score: {doc['search_score']}"
            )


def retrieval_relevant_documents(client: AtlasClient, query_text: str, index_name: str, embed_field: str, model_name: str):
    """
    Executes a vector search on MongoDB Atlas.

    Args:
        client (AtlasClient): MongoDB client.
        query_text (str): The text to search for.
        index_name (str): Name of the MongoDB Atlas index.
        embed_field (str): Name of the embedding field in MongoDB.
        model_name (str): Name of the embedding model.
    
    Returns:
        list: List of relevant documents retrieved from MongoDB Atlas.
    """
    logger.info("Starting vector search with MongoDB Atlas.")

    model = initialize_model(model_name)
    query_embedding = generate_query_embedding(model, query_text)
    search_results = run_vector_search(client, index_name, embed_field, query_embedding)

    log_search_results(search_results)

    return search_results
