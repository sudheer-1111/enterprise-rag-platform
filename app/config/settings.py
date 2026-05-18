from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_env: str

    model_provider: str
    ollama_base_url: str

    chat_model: str
    backup_chat_model: str
    embedding_model: str

    mongodb_uri: str
    mongodb_database: str

    vector_store_type: str
    chroma_db_path: str
    raw_data_path: str
    processed_data_path: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()