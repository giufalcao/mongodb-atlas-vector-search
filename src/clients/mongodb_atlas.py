from sys import exception
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from typing import List, Dict, Optional
from loguru import logger
import time

class AtlasClient:
    """
    Class for interacting with MongoDB Atlas, encapsulating common operations.
    """

    def __init__(self, atlas_uri: str, database_name: str, collection_name: str):
        """
        Initializes the MongoDB Atlas client.

        Args:
            atlas_uri (str): MongoDB Atlas connection URI.
            database_name (str): Database name.
            collection_name (str): Collection name.
        """
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[database_name]
        self.collection = self.database[collection_name]


    def ping(self) -> None:
        """Tests the connection to MongoDB Atlas."""
        try:
            self.mongodb_client.admin.command("ping")
            print("Successfully connected to MongoDB Atlas.")
        except Exception as e:
            print(f"Error connecting to MongoDB Atlas: {e}")

    
    def set_collection(self, collection_name: str) -> None:
        """
        Sets the collection to be used in the database.

        Args:
            collection_name (str): The name of the collection.
        """
        self.collection = self.database[collection_name]
        return
    

    def find(self, filter: Optional[Dict] = None, projection: Optional[Dict] = None, limit: int = 0) -> List[Dict]:
        """
        Finds documents in a collection with an optional filter, projection, and limit.

        Args:
            filter (Optional[Dict]): Filter for the query.
            projection (Optional[Dict]): Fields to include or exclude (default: None).
            limit (int): Maximum number of documents to return.

        Returns:
            List[Dict]: List of found documents with the specified projection.
        """
        return list(self.collection.find(filter or {}, projection or {}, limit=limit))


    def create_vector_search_index(self, index_name: str, vector_field: str, dimensions: int, similarity_metric: str, quantization: str) -> None:
        """
        Creates a vector search index on the specified collection.
        
        Args:
            index_name (str): The desired name for the vector search index.
            vector_field (str): The field in the documents that contains the vector embeddings.
            dimensions (int): The dimensionality of the vector embeddings.
            similarity_metric (str): The similarity metric to use (e.g., cosine, dotProduct, euclidean).
            quantization (str): The quantization method to apply (e.g., 'none', 'scalar', 'product').
        """
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": vector_field,
                        "numDimensions": dimensions,
                        "similarity": similarity_metric,
                        "quantization": quantization,
                    }

                ]
            },
            name=index_name,
            type="vectorSearch"
        )
            
        try:
            result = self.collection.create_search_index(search_index_model)
            logger.info(f"New search index '{result}' created.")
        except Exception as e:
            logger.error(f"Error creating search index: {e}")
            return

        logger.info("Polling to check if the index is ready. This may take up to a minute.")
        predicate = lambda index: index.get("queryable") is True
        
        while True:
            indices = list(self.collection.list_search_indexes(result))
            if indices and predicate(indices[0]):
                break
            time.sleep(5)
        
        logger.info(f"{result} is ready for querying.")
        return


    def run_vector_search_index(self, index_name: str, attr_name: str, embedding_vector: List[float], limit: int = 5) -> List[Dict]:
        """
        Performs a vector search in the specified collection.

        Args:
            collection_name (str): Collection name.
            index_name (str): Vector search index name.
            attr_name (str): Attribute storing vector embeddings.
            embedding_vector (List[float]): Query vector.
            limit (int): Maximum number of results to return.

        Returns:
            List[Dict]: List of search results.
        """
        results = self.collection.aggregate([
            {
                '$vectorSearch': {
                    "index": index_name,
                    "path": attr_name,
                    "queryVector": embedding_vector,
                    "numCandidates": 50,
                    "limit": limit,
                }
            },
            {
                "$project": {
                    '_id': 1,
                    'title': 1,
                    'plot': 1,
                    'year': 1,
                    "search_score": {"$meta": "vectorSearchScore"}
                }
            }
        ])
        return list(results)
    

    def close_connection(self) -> None:
        """Closes the MongoDB connection."""
        self.mongodb_client.close()
        print("MongoDB connection closed.")