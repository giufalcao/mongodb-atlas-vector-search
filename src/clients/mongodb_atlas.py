from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from pymongo.database import Database
from typing import List, Dict, Optional

class AtlasClient:
    """
    Class for interacting with MongoDB Atlas, encapsulating common operations.
    """

    def __init__(self, atlas_uri: str, dbname: str):
        """
        Initializes the MongoDB Atlas client.

        Args:
            atlas_uri (str): MongoDB Atlas connection URI.
            dbname (str): Database name.
        """
        self.mongodb_client = MongoClient(atlas_uri)
        self.database = self.mongodb_client[dbname]


    def ping(self) -> None:
        """Tests the connection to MongoDB Atlas."""
        try:
            self.mongodb_client.admin.command("ping")
            print("Successfully connected to MongoDB Atlas.")
        except Exception as e:
            print(f"Error connecting to MongoDB Atlas: {e}")

    def get_database(self) -> Database:
        """
        Retrieves the database object.

        Returns:
            Database: The MongoDB database object.
        """
        return self.database


    def get_collection(self, collection_name: str):
        """Retrieves a collection from the database."""
        return self.database[collection_name]


    def find(self, collection_name: str, filter: Optional[Dict] = None, limit: int = 10) -> List[Dict]:
        """
        Finds documents in a collection with an optional filter and limit.

        Args:
            collection_name (str): Collection name.
            filter (Optional[Dict]): Filter for the query.
            limit (int): Maximum number of documents to return.

        Returns:
            List[Dict]: List of found documents.
        """
        collection = self.get_collection(collection_name)
        return list(collection.find(filter or {}, limit=limit))


    def create_vector_index(self, collection_name: str, search_index_model: SearchIndexModel) -> None:
        """Creates a vector search index on the specified collection."""
        collection = self.get_collection(collection_name)
        try:
            result = collection.create_search_index(model=search_index_model)
            print(f"New search index '{result}' created.")
        except Exception as e:
            print(f"Error creating search index: {e}")


    def vector_search(self, collection_name: str, index_name: str, attr_name: str, embedding_vector: List[float], limit: int = 5) -> List[Dict]:
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
        collection = self.get_collection(collection_name)
        results = collection.aggregate([
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