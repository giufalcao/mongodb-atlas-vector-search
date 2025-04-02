from loguru import logger
import pymongo
from sentence_transformers import SentenceTransformer

from src.clients.mongodb_atlas import AtlasClient
from src.common.model import get_embedding, initialize_model


def fetch_documents(client: AtlasClient, field_to_embed: str, batch_size: int):
    """Fetches documents from MongoDB that require embeddings."""
    logger.info(f"Fetching up to {batch_size} documents from Atlas...")
    field_to_return = {"_id": 1, field_to_embed: 1}
    filter_documents = {field_to_embed: {"$exists": True}}

    documents = list(client.find(
        filter=filter_documents,
        projection=field_to_return,
        limit=batch_size
    ))

    logger.info(f"Fetched {len(documents)} documents.")
    return documents


def generate_embeddings(model: SentenceTransformer, documents: list, field_to_embed: str):
    """Generates embeddings for a batch of documents."""
    logger.info("Generating embeddings for documents...")
    for doc in documents:
        doc["embedding"] = get_embedding(model, doc[field_to_embed])
    logger.info("Embeddings generated.")
    return documents


def update_documents(client: AtlasClient, documents: list, embed_field: str):
    """Performs a bulk update of documents in MongoDB."""
    if not documents:
        return

    logger.info(f"Updating {len(documents)} documents in MongoDB...")
    updates = [
        pymongo.UpdateOne({"_id": doc["_id"]}, {"$set": {embed_field: doc["embedding"]}})
        for doc in documents
    ]

    collection = client.database["new_collection"]

    collection.bulk_write(updates)
    logger.info("Documents successfully updated.")


def ingest_embeddings(client: AtlasClient, field_to_embed: str, embed_field: str, model_name: str, batch_size: int = 100):
    """
    Reads documents from Atlas, generates embeddings using the specified model,
    and updates the documents with the generated embeddings.

    Args:
        client (AtlasClient): MongoDB client object.
        field_to_embed (str): The field containing the text to embed.
        embed_field (str): The field to store the generated embeddings.
        model_name (str): Name of the embedding model.
        batch_size (int): Number of documents to process per batch. Default is 100.
    """
    model = initialize_model(model_name)
    total_processed = 0

    while True:
        documents = fetch_documents(client, field_to_embed, batch_size)
        if not documents:
            break 

        documents = generate_embeddings(model, documents, field_to_embed)
        update_documents(client, documents, embed_field)

        total_processed += len(documents)
        logger.info(f"Total processed: {total_processed}")

    logger.info(f"Embedding ingestion completed. Total documents processed: {total_processed}")
