from loguru import logger
import pymongo
from pymongo.operations import UpdateOne
from sentence_transformers import SentenceTransformer


from src.clients.mongodb_atlas import AtlasClient
from src.common.model import get_embedding, initialize_model


def fetch_documents(client: AtlasClient, field_to_embed: str,  embed_field: str, batch_size: int):
    """Fetches documents from MongoDB that require embeddings."""
    logger.info(f"Fetching up to {batch_size} documents from Atlas...")
    documents_filter = {"_id": 1, field_to_embed: 1}
    filter_documents = {
        field_to_embed: {"$exists": True},
        embed_field: {"$exists": False}
    }

    documents = client.find(
        filter=filter_documents,
        projection=documents_filter,
        limit=batch_size
    )

    if len(list(documents)) == 0:
        logger.info(f"All '{field_to_embed}' fields have their corresponding embedding fields.")
        return []

    logger.info(f"Fetched {len(list(documents))} documents.")
    return documents


def update_documents(client: AtlasClient, model, documents: list, field_to_embed: str, embed_field: str):
    """Performs a bulk update of documents in MongoDB."""
    if not documents:
        return

    logger.info(f"Updating {len(documents)} documents in MongoDB...")
    operations = []
    for doc in documents:
        raw_data = doc[field_to_embed]
        embedding = get_embedding(model, raw_data)
        operations.append(UpdateOne(
            {"_id": doc["_id"]},
            {"$set": {
                embed_field: embedding
            }}
        ))

    client.collection.bulk_write(operations)
    logger.info("Documents successfully updated.")


def ingest_embeddings(client: AtlasClient, field_to_embed: str, embed_field: str, model_name: str, batch_size: int = 250):
    """
    Reads documents from Atlas, generates embeddings using the specified model,
    and updates the documents with the generated embeddings.

    Args:
        client (AtlasClient): MongoDB client object.
        field_to_embed (str): The field containing the text to embed.
        embed_field (str): The field to store the generated embeddings.
        model_name (str): Name of the embedding model.
        batch_size (int): Number of documents to process per batch. Default is 500.
    """
    model = initialize_model(model_name)
    total_processed = 0

    while True:
        documents = fetch_documents(client, field_to_embed, embed_field, batch_size)
        if not documents:
            break 

        update_documents(client, model, documents, field_to_embed, embed_field)

        total_processed += len(documents)
        logger.info(f"Total processed: {total_processed}")

    logger.info(f"Embedding ingestion completed. Total documents processed: {total_processed}")
