from openai import OpenAI
from typing import List, Dict, Literal, Union

from openai.types.chat.chat_completion import ChatCompletion


class OpenAIClient:
    """
    A wrapper class for the OpenAI API, providing chat completion and embedding functionalities.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes the OpenAIClient with the provided API key.

        Args:
            api_key: The OpenAI API key.
        """
        self.client = OpenAI(api_key=api_key)

    def chat(self, messages, model: str = "gpt-3.5-turbo") -> ChatCompletion | None:
        """
        Generates a chat completion using the OpenAI API.

        Args:
            messages: A list of message dictionaries, each containing 'role' and 'content'.
            model: The name of the model to use for chat completion.

        Returns:
            The chat completion response from the OpenAI API.
        """
        try:
            chat_completion = self.client.chat.completions.create(messages=messages, model=model)
            return chat_completion
        except Exception as e:
            print(f"Error during chat completion: {e}")
            return None

    def get_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float] | None:
        """
        Generates an embedding for the given text using the OpenAI API.

        Args:
            text: The text to embed.
            model: The name of the model to use for embedding.

        Returns:
            A list of floats representing the embedding of the text.
        """
        try:
            text = text.replace("\n", " ")
            resp = self.client.embeddings.create(input=[text], model=model)
            return resp.data[0].embedding
        except Exception as e:
            print(f"Error during embedding generation: {e}")
            return None