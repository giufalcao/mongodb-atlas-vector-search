import logging
from sentence_transformers import SentenceTransformer

from src.clients.mongodb_atlas import AtlasClient
from src.common.embedding import get_embedding

def ingest_embeddings(client: AtlasClient, vector_to_embed: str, vector_field: str, model: str) -> None:
    """
    Reads documents from Atlas, generates embeddings using Nomic AI model,
    and updates the documents with the generated embeddings.

    Args:
        client (AtlasClient): MongoDB client object.
        vector_to_embed (str): The field containing the text to embed.
        vector_field (str): The field to store the generated embeddings.
        model (str): Configuration object containing model information.
    """

    logger = logging.getLogger(__name__)

    logger.info("Reading documents from Atlas...")
    field_to_return = {"_id": 1, vector_to_embed: 1}
    filter_documents = {vector_to_embed: {"$exists": True}}
    documents = list(client.find(
        filter=filter_documents,
        projection=field_to_return
    ))
    logger.info(f"Documents read completed. Len: {len(documents)}.")

    logger.info("Generating embeddings...")
    model = SentenceTransformer(model, trust_remote_code=True) # type: ignore
    for doc in documents:
        doc["embedding"] = get_embedding(model, doc[vector_to_embed])
    logger.info("Embeddings generated.")

    logger.info("Updating documents with embeddings in Atlas...")
    for doc in documents:
        client.collection.update_one({"_id": doc["_id"]}, {"$set": {vector_field: doc["embedding"]}})

    logger.info("Embeddings successfully stored in Atlas.")
    return