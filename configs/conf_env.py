from loguru import logger
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    A Pydantic-based settings class for managing application configurations.
    """

    # --- Pydantic Settings ---
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # --- MongoDB Atlas Configuration ---
    MONGODB_DATABASE_NAME: str = Field(
        default="",
        description="Name of the MongoDB database.",
    )
    MONGODB_URI: str = Field(
        default="",
        description="Connection URI for the local MongoDB Atlas instance.",
    )

    MONGODB_COLLECTION_NAME: str = Field(
        default="",
        description="Collection name for the local MongoDB Atlas instance.",
    )

    MONGODB_INDEX_NAME: str = Field(
        default="",
        description="Index name for searching in the local MongoDB Atlas instance.",
    )

    MONGODB_ATTRIBUTE_NAME: str = Field(
        default="",
        description="Attribute storing vector embeddings for the local MongoDB Atlas instance.",
    )

    @field_validator("MONGODB_DATABASE_NAME", "MONGODB_URI", "MONGODB_COLLECTION_NAME")
    @classmethod
    def check_not_empty(cls, value: str, info) -> str:
        if not value or value.strip() == "":
            logger.error(f"{info.field_name} cannot be empty.")
            raise ValueError(f"{info.field_name} cannot be empty.")
        return value


try:
    settings = Settings()
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    raise SystemExit(e)