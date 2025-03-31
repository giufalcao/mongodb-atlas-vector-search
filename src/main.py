import sys
import argparse
from loguru import logger

from configs import conf_embedding, conf_env
from clients.mongodb_atlas import AtlasClient, SearchIndexModel
from infrastructure.create_atlas_search_index import setup_vector_index


def parse_args(parsed_args, client: AtlasClient, index_name: str, vector_field: str, dimensions: int, similarity_metric: str):
    """
    Parses command-line arguments and sets up the vector index if requested.

    Args:
        parsed_args (argparse.Namespace): The parsed command-line arguments.
        client (AtlasClient): The MongoDB Atlas client instance.
        index_name (str): The desired name for the vector search index.
        vector_field (str): The field in the documents that contains the vector embeddings.
        dimensions (int): The dimensionality of the vector embeddings.
        similarity_metric (str): The similarity metric to use.
    """
    if parsed_args.setup_search_index:
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
        logger.info("Using existent collection defined in .env")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MongoDB Atlas Vector Search Example")
    parser.add_argument("--setup_search_index", action="store_true", default=False, help="Setup the vector index")
    parser.add_argument("--index_name", type=str, default="test_vector_index", help="Name of the vector index")
    parser.add_argument("--vector_field", type=str, default="plot_embedding", help="Field containing vector embeddings")
    parser.add_argument("--dimensions", type=int, default=1536, help="Dimensionality of vector embeddings")
    parser.add_argument("--similarity_metric", type=str, default="dotProduct", help="Similarity metric (cosine, dotProduct, euclidean)")
    parsed_args = parser.parse_args(sys.argv[1:])

    client = AtlasClient(conf_env.settings.MONGODB_URI, conf_env.settings.MONGODB_DATABASE_NAME)
    client.ping()

    parse_args(parsed_args, client, parsed_args.index_name, parsed_args.vector_field, parsed_args.dimensions, parsed_args.similarity_metric)

    # Find and print some sample movies
    try:
        logger.info(f"Finding 5 sample movies.")
        movies = client.find(collection_name=conf_env.settings.MONGODB_COLLECTION_NAME, limit=5)
        if movies:
            logger.info(f"Found {len(movies)} movies.")
            for idx, movie in enumerate(movies):
                print(f'{idx+1}\nid: {movie["_id"]}\ntitle: {movie["title"]},\nyear: {movie["year"]}\nplot: {movie["plot"]}\n')
        else:
            logger.warning("No movies found.")
    except Exception as e:
        logger.error(f"Error finding and printing movies: {e}")

    results = client.vector_search(
        conf_env.settings.MONGODB_COLLECTION_NAME,
        conf_env.settings.MONGODB_INDEX_NAME,
        conf_env.settings.MONGODB_ATTRIBUTE_NAME,
        conf_embedding.EMBEDDING_VECTOR,
    )

    for result in results:
        print(result)

    client.close_connection()