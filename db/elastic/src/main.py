#!/usr/bin/env python3
"""
Инициализация индексов Elasticsearch из JSON схем
"""
import json
import time
import logging
from pathlib import Path
import sys
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
from config import settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Глобальный клиент
es_client = None


def get_elasticsearch_client() -> Elasticsearch:
    """Получение или создание клиента Elasticsearch"""
    global es_client
    if es_client is None:
        es_client = Elasticsearch(
            hosts=[f"http://{settings.es_host}:{settings.es_port}"],
            basic_auth=("elastic", settings.es_password),
            request_timeout=10
        )
    return es_client


def wait_for_elasticsearch() -> bool:
    """Ожидание доступности Elasticsearch"""
    logger.info(f"Waiting for Elasticsearch at http://{settings.es_host}:{settings.es_port}...")
    
    client = get_elasticsearch_client()
    
    for attempt in range(settings.max_retries):
        try:
            info = client.info()
            logger.info(f"✓ Elasticsearch is ready (version {info['version']['number']})")
            return True
        except ConnectionError as e:
            logger.debug(f"Attempt {attempt + 1}/{settings.max_retries} failed: {e}")
            time.sleep(settings.retry_delay)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(settings.retry_delay)
    
    logger.error("Failed to connect to Elasticsearch")
    return False


def create_index(client: Elasticsearch, index_name: str, schema: dict) -> bool:
    """Создание индекса"""
    try:
        # Проверка существования индекса
        if client.indices.exists(index=index_name):
            logger.info(f"✓ Index '{index_name}' already exists")
            return True
        
        # Создание индекса
        response = client.indices.create(index=index_name, body=schema)
        logger.info(f"✓ Index '{index_name}' created successfully")
        return True
        
    except Exception as e:
        logger.error(f"✗ Error creating index '{index_name}': {e}")
        return False


def init_indices() -> bool:
    """Инициализация всех индексов"""
    # Ищем схемы в разных местах
    possible_dirs = [
        Path(__file__).parent,  # Если скрипт в папке со схемами
        Path("/app"),  # Если запущено в контейнере
        Path("/app/db/elastic"),  # Альтернативная папка в контейнере
    ]
    
    schemas_dir = None
    for dir_path in possible_dirs:
        schema_files = sorted(dir_path.glob("schema_*.json"))
        if schema_files:
            schemas_dir = dir_path
            break
    
    if schemas_dir is None:
        logger.warning("No schema files found in any location")
        return False
    
    schema_files = sorted(schemas_dir.glob("schema_*.json"))
    logger.info(f"Loading schemas from {schemas_dir}")
    logger.info(f"Found {len(schema_files)} schema files")
    
    client = get_elasticsearch_client()
    success_count = 0
    
    for schema_file in schema_files:
        index_name = schema_file.stem.replace("schema_", "")
        
        try:
            with open(schema_file) as f:
                schema = json.load(f)
            
            if create_index(client, index_name, schema):
                success_count += 1
        except Exception as e:
            logger.error(f"✗ Error processing {schema_file.name}: {e}")
    
    logger.info(f"Initialization complete: {success_count}/{len(schema_files)} indices created")
    return success_count == len(schema_files)


if __name__ == "__main__":
    try:
        if not wait_for_elasticsearch():
            sys.exit(1)
        
        if not init_indices():
            sys.exit(1)
        
        logger.info("✓ All done!")
        sys.exit(0)
    finally:
        if es_client:
            es_client.close()
