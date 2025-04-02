import logging
from sentence_transformers import SentenceTransformer

from src.clients.mongodb_atlas import AtlasClient
from src.common.embedding import get_embedding

def retrieval_relevant_documents(client: AtlasClient, query_text: str, index_name: str, vector_field: str, model: str):
    """Executa a busca vetorial no MongoDB Atlas."""
    logger = logging.getLogger(__name__)
    
    logger.info("Starting vector search with MongoDB Atlas.")
    model = SentenceTransformer(model, trust_remote_code=True)  # type: ignore
    embedding = get_embedding(model, query_text)
    
    logger.info(f"Performing vector search for query: '{query_text}'")
    movies = client.run_vector_search_index(index_name, vector_field, embedding)
    
    if movies:
        logger.info(f"Vector search returned {len(movies)} results.")
        for movie in movies:
            logger.info(
                f"Movie ID: {movie['_id']} | Title: {movie['title']} | "
                f"Year: {movie['year']} | Search Score: {movie['search_score']}"
            )
    else:
        logger.warning("No movies found in vector search.")
    
    return movies