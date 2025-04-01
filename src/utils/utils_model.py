from typing import List


# Define a function to generate embeddings (moved outside functions)
def get_embedding(model, data: str, precision: str = "float32") -> List[float]:
    """Generates an embedding for the given text."""
    return model.encode(data, precision=precision).tolist()