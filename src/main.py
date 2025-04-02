import sys
import argparse
from loguru import logger
import numpy as np
from sentence_transformers import SentenceTransformer

from configs import conf_models, conf_env
from clients.mongodb_atlas import AtlasClient
from src.retrieval import retrieval
from src.ingestion import ingestion


def parse_args(
    create_vetor_search_index: str,
    field_to_embed: str,
    index_name: str, 
    embed_field: str, 
    dimensions: int, 
    similarity_metric: str,
    quantization: str
) -> tuple[str, str, str, str, int, str, str]:
    """
    Parses command-line arguments and sets up the vector index if requested.
    Returns all arguments as individual values.
    """
    create_vetor_search_index_value = create_vetor_search_index
    field_to_embed_value = field_to_embed
    index_name_value = index_name
    embed_field_value = embed_field
    dimensions_value = dimensions
    similarity_metric_value = similarity_metric
    quantization_value = quantization
    
    logger.info(f"Create Vector Search Index: {create_vetor_search_index_value}")
    logger.info(f"Column to be embeded: {field_to_embed}")
    logger.info(f"Index Name: {index_name_value}")
    logger.info(f"Embed Field name: {embed_field_value}")
    logger.info(f"Dimensions: {dimensions_value}")
    logger.info(f"Similarity Metric: {similarity_metric_value}")
    logger.info(f"Quantization strategy: {quantization_value}")


    return (
        create_vetor_search_index_value,
        field_to_embed_value,
        index_name_value, 
        embed_field_value, 
        dimensions_value, 
        similarity_metric_value,
        quantization_value
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MongoDB Atlas Vector Search Example")
    parser.add_argument("--create_vetor_search_index", type=bool, default=False, help="Create Vector Search Index")
    parser.add_argument("--field_to_embed", type=str, default="plot", help="Name of the column we want to embed")
    parser.add_argument("--index_name", type=str, default="test_vector_index", help="Name of the vector index")
    parser.add_argument("--embed_field", type=str, default="new_embedding", help="Field containing vector embeddings")
    parser.add_argument("--dimensions", type=int, default=768, help="Dimensionality of vector embeddings")
    parser.add_argument("--similarity_metric", type=str, default="dotProduct", help="Similarity metric (cosine, dotProduct, euclidean)")
    parser.add_argument("--quantization", type=str, default="scalar", help="Qantization method to apply (e.g., 'none', 'scalar', 'product').")
    parsed_args = parser.parse_args(sys.argv[1:])

    logger.info("Initializing MongoDB Atlas client...")
    client = AtlasClient(
        conf_env.settings.MONGODB_URI,
        conf_env.settings.MONGODB_DATABASE_NAME,
        conf_env.settings.MONGODB_COLLECTION_NAME
    )
    client.ping()
    logger.info("MongoDB Atlas client initialized.")
    
    (   
        create_vetor_search_index,
        field_to_embed,
        index_name, 
        embed_field, 
        dimensions, 
        similarity_metric ,
        quantization
    ) = parse_args(
        parsed_args.create_vetor_search_index,
        parsed_args.field_to_embed,
        parsed_args.index_name,
        parsed_args.embed_field,
        parsed_args.dimensions,
        parsed_args.similarity_metric,
        parsed_args.quantization
    )

    logger.info("Data preparation and ingestion starting...")
    ingestion.ingest_embeddings(
        client,
        field_to_embed,
        embed_field,
        conf_models.NOMIC_AI_EMBED_TEXT_V1
    )
    logger.info("Data preparation and ingestion finished.")
    logger.critical("This will not work on free tier clusters.")

    if create_vetor_search_index:
        logger.info("Creating Vector Search Index...")
        logger.critical("This will not work on free tier clusters.")
        client.create_vector_search_index(
            index_name,
            embed_field,
            dimensions,
            similarity_metric,
            quantization

        )
        logger.info("Vector Search Index setup complete.")
    else:
        logger.info("Using existing collection defined in .env")

    logger.info("Data retrieval starting...")
    user_input_text = "humans fighting"
    movies = retrieval.retrieval_relevant_documents(
        client, 
        user_input_text,
        index_name, 
        embed_field, 
        conf_models.NOMIC_AI_EMBED_TEXT_V1
    )
    logger.info("Data retrieval finished.")

    client.close_connection()
    logger.info("MongoDB Atlas client connection closed.")