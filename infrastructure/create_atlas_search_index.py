from clients.mongodb_atlas import AtlasClient, SearchIndexModel

def setup_vector_index(client: AtlasClient, collection_name: str, index_name: str, vector_field: str, dimensions: int, similarity_metric: str = "cosine") -> None:
    """
    Sets up a vector search index on a MongoDB Atlas collection.

    Args:
        client (AtlasClient): The MongoDB Atlas client instance.
        collection_name (str): The name of the collection to create the index on.
        index_name (str): The desired name for the vector search index.
        vector_field (str): The field in the documents that contains the vector embeddings.
        dimensions (int): The dimensionality of the vector embeddings.
        similarity_metric (str, optional): The similarity metric to use (default is "cosine").
                                          Other valid options include "dotProduct" and "euclidean".
    """
    index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": vector_field,
                    "numDimensions": dimensions,
                    "similarity": similarity_metric,
                    "quantization": "scalar"
                }
            ]
        },
        name=index_name,
        type="vectorSearch"
    )
    client.create_vector_index(collection_name, index_model)