from pydantic_settings import BaseSettings


class Config(BaseSettings):
    es_port: str = "9200"
    es_host: str = "elasticsearch"
    es_password: str = "elasticsearch_secret_password_123"

    max_retries: int = 30
    retry_delay: int = 2

settings = Config()
