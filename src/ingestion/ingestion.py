from pymongo import UpdateOne
from sentence_transformers import SentenceTransformer
from src.clients.mongodb_atlas import AtlasClient
from typing import List, Dict, Optional

from src.utils import utils_model


def get_embedded_movies_with_summary(
    atlas_client: AtlasClient,
    collection_name: str = "embedded_movies",
    limit: int = 50
) -> List[Dict]:
    """
    Retrieves a subset of embedded movies from a MongoDB collection that have a non-null and non-empty 'summary' field.

    Args:
        atlas_client (AtlasClient): An instance of the AtlasClient class.
        collection_name (str, optional): The name of the collection. Defaults to "embedded_movies".
        database_name (str, optional): The name of the database. Defaults to "sample_mflix".
        limit (int, optional): The maximum number of documents to retrieve. Defaults to 50.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary represents a document with '_id' and 'summary' fields.
                   Returns an empty list if an error occurs during the query.
    """
    try:
        collection = atlas_client.get_collection(collection_name)
        filter_query = {"summary": {"$exists": True, "$nin": [None, ""]}}
        documents = collection.find(filter_query, {"_id": 1, "summary": 1}).limit(limit)
        return [{"_id": doc["_id"], "summary": doc["summary"]} for doc in documents]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def update_embedded_movies_with_embeddings(
    atlas_client: AtlasClient,
    documents: List[Dict],
    collection_name: str,
    model,
) -> Optional[int]:
    """
    Updates embedded movies with embeddings generated from their summaries.

    Args:
        atlas_client (AtlasClient): An instance of the AtlasClient class.
        documents (List[Dict]): A list of documents with _id and summary.
        collection_name (str, optional): The name of the collection. Defaults to "embedded_movies".
        database_name (str, optional): The name of the database. Defaults to "sample_mflix".

    Returns:
        Optional[int]: The number of documents updated. Returns None if an error occurs.
    """
    try:
        operations = [
            UpdateOne({"_id": doc["_id"]}, {"$set": {"embedding": utils_model.get_embedding(model,doc["summary"])}})
            for doc in documents
        ]

        if operations:
            collection = atlas_client.get_collection(collection_name)
            result = collection.bulk_write(operations)
            updated_doc_count = result.modified_count
            print(f"Updated {updated_doc_count} documents.")
            return updated_doc_count
        else:
            print("No documents to update.")
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
