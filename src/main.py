import sys
import argparse
from loguru import logger
from sentence_transformers import SentenceTransformer

from configs import conf_embedding, conf_env
from clients.mongodb_atlas import AtlasClient
from infrastructure.create_atlas_search_index import setup_vector_index
from retrieval import retrieval


def parse_args(client: AtlasClient, setup_search_index: bool, index_name: str, vector_field: str, dimensions: int, similarity_metric: str):
    """
    Parses command-line arguments and sets up the vector index if requested.
    """
    if setup_search_index:
        logger.info("Setting up vector index...")
        setup_vector_index(
            client,
            conf_env.settings.MONGODB_COLLECTION_NAME,
            index_name,
            vector_field,
            dimensions,
            similarity_metric
        )
        logger.info("Vector index setup complete.")
    else:
        logger.info("Using existing collection defined in .env")


def find_sample_movies(client: AtlasClient):
    """
    Finds and logs sample movies from the collection.
    """
    try:
        logger.info("Fetching 5 sample movies...")
        movies = client.find(collection_name=conf_env.settings.MONGODB_COLLECTION_NAME, limit=5)
        if movies:
            logger.info(f"Found {len(movies)} movies.")
            for movie in movies:
                logger.info(f"Movie ID: {movie['_id']} | Title: {movie['title']} | Year: {movie['year']}")
        else:
            logger.warning("No movies found.")
    except Exception as e:
        logger.error(f"Error finding and logging movies: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MongoDB Atlas Vector Search Example")
    parser.add_argument("--setup_search_index", action="store_true", default=False, help="Setup the vector index")
    parser.add_argument("--index_name", type=str, default="test_vector_index", help="Name of the vector index")
    parser.add_argument("--vector_field", type=str, default="plot_embedding", help="Field containing vector embeddings")
    parser.add_argument("--dimensions", type=int, default=1536, help="Dimensionality of vector embeddings")
    parser.add_argument("--similarity_metric", type=str, default="dotProduct", help="Similarity metric (cosine, dotProduct, euclidean)")
    parsed_args = parser.parse_args(sys.argv[1:])

    logger.info("Initializing MongoDB Atlas client...")
    client = AtlasClient(conf_env.settings.MONGODB_URI, conf_env.settings.MONGODB_DATABASE_NAME)
    client.ping()

    logger.info("Starting basic search with MongoDB Atlas.")
    parse_args(
        client,
        parsed_args.setup_search_index,
        parsed_args.index_name,
        parsed_args.vector_field,
        parsed_args.dimensions,
        parsed_args.similarity_metric
    )

    find_sample_movies(client)

    logger.info("Starting vector search with MongoDB Atlas.")
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    user_input_text = "beach house"
    embedding = retrieval.get_embedding(model, user_input_text)

    logger.info(f"Performing vector search for query: '{user_input_text}'")
    movies = retrieval.perform_vector_search(client, embedding)

    if movies:
        logger.info(f"Vector search returned {len(movies)} results.")
        for movie in movies:
            logger.info(f"Movie ID: {movie['_id']} | Title: {movie['title']} | Year: {movie['year']} | Search Score: {movie['search_score']}")
    else:
        logger.warning("No movies found in vector search.")

    client.close_connection()
    logger.info("MongoDB Atlas client connection closed.")