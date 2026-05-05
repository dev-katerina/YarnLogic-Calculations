from pydantic_settings import BaseSettings

class Config(BaseSettings):
    graphdb_host: str = "graphdb"
    graphdb_port: int = 7687
    graphdb_user: str = "neo4j"
    graphdb_password: str = "testpassword"


settings = Config()