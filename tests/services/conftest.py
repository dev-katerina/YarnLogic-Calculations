import pytest
from unittest.mock import AsyncMock, MagicMock
from service.graph_manager import GraphManager


@pytest.fixture
def mock_driver():
    """Создает mock Neo4j драйвера"""
    return MagicMock()


@pytest.fixture
def mock_session():
    """Создает mock сессии Neo4j"""
    return AsyncMock()


@pytest.fixture
def mock_result():
    """Создает mock результата запроса"""
    return AsyncMock()


@pytest.fixture
def graph_manager(mock_driver):
    """Создает экземпляр GraphManager с mock драйвером"""
    return GraphManager(mock_driver)
