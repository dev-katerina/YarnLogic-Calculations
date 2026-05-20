from pydantic_settings import BaseSettings


class Config(BaseSettings):
    graphdb_host: str = "graphdb"
    graphdb_port: int = 7687
    graphdb_user: str = "neo4j"
    graphdb_password: str = "testpassword"

    postgres_user: str = "postgres"
    postgres_password: str = "testpassword"
    postgres_host: str = "postgres"
    postgres_port: str = "5432"
    postgres_db: str = "yarnlogic"
    postgres_schema: str = "yarnlogic_calculate"


settings = Config()
