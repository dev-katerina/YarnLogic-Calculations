import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from models.neo4j import Stitch, Relation


class TestAddNode:
    """Тесты для метода add_node"""

    @pytest.mark.parametrize(
        "node_data",
        [
            Stitch(id=uuid4(), type="stitch", tool="test_tool", graph_id=uuid4()),
            Stitch(id=uuid4(), type="", tool="", graph_id=uuid4()),
        ],
    )
    @pytest.mark.asyncio
    async def test_add_node_success(
        self, graph_manager, mock_session, mock_result, node_data
    ):
        """Тест успешного добавления узла"""
        mock_record = node_data.dict()

        mock_result.single = AsyncMock(return_value=mock_record)
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.add_node(node_data)

        # Assert
        assert result == mock_record
        mock_session.run.assert_called_once()
        assert "CREATE (n:Node $props)" in mock_session.run.call_args[0][0]

    @pytest.mark.parametrize(
        "node_data",
        [
            "invalid_node_data",
            None,
            123,
        ],
    )
    @pytest.mark.asyncio
    async def test_add_node_value_error(
        self, graph_manager, mock_session, mock_result, node_data
    ):
        """Тест добавления узла с некорректными данными"""
        # Act & Assert
        with pytest.raises(ValueError):
            await graph_manager.add_node(node_data)


class TestAddRelationship:
    """Тесты для метода add_relationship"""

    @pytest.mark.parametrize(
        "from_id,to_id,properties",
        [
            (uuid4(), uuid4(), Relation(id=uuid4(), type="connects", graph_id=uuid4())),
        ],
    )
    @pytest.mark.asyncio
    async def test_add_relationship_success(
        self, graph_manager, mock_session, mock_result, from_id, to_id, properties
    ):
        """Тест успешного добавления связи"""
        # Arrange
        mock_result.single = AsyncMock(return_value={"r": "relationship"})
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.add_relationship(from_id, to_id, properties)

        # Assert
        assert result == {"r": "relationship"}
        mock_session.run.assert_called_once()
        call_args = mock_session.run.call_args
        assert call_args[1]["from_id"] == from_id
        assert call_args[1]["to_id"] == to_id

    @pytest.mark.parametrize(
        "from_id,to_id,properties",
        [
            (uuid4(), uuid4(), None),
            (uuid4(), uuid4(), "invalid_properties"),
            (uuid4(), uuid4(), 123),
        ],
    )
    @pytest.mark.asyncio
    async def test_add_relationship_value_error(
        self, graph_manager, from_id, to_id, properties
    ):
        """Тест добавления связи с некорректными данными"""
        # Act & Assert
        with pytest.raises(ValueError):
            await graph_manager.add_relationship(from_id, to_id, properties)


class TestQueryGraph:
    """Тесты для метода query_graph"""

    @pytest.mark.asyncio
    async def test_query_graph_success(self, graph_manager, mock_session, mock_result):
        """Тест успешного запроса графа"""
        # Arrange
        graph_id = uuid4()
        node_id = uuid4()
        expected_records = [
            {
                "n": {
                    "id": str(node_id),
                    "type": "stitch",
                    "tool": "tool",
                    "graph_id": str(graph_id),
                }
            }
        ]
        mock_result.values = AsyncMock(return_value=expected_records)
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.query_graph(graph_id)

        # Assert
        assert result == expected_records
        mock_session.run.assert_called_once()
        assert mock_session.run.call_args[1]["graph_id"] == graph_id

    @pytest.mark.asyncio
    async def test_query_graph_empty_result(
        self, graph_manager, mock_session, mock_result
    ):
        """Тест запроса графа с пустым результатом"""
        # Arrange
        graph_id = uuid4()
        mock_result.values = AsyncMock(return_value=[])
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.query_graph(graph_id)

        # Assert
        assert result == []
        mock_session.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_query_graph_with_multiple_nodes(
        self, graph_manager, mock_session, mock_result
    ):
        """Тест запроса графа с несколькими узлами"""
        # Arrange
        graph_id = uuid4()
        expected_records = [
            {
                "n": {
                    "id": str(uuid4()),
                    "type": "stitch",
                    "tool": "tool",
                    "graph_id": str(graph_id),
                }
            }
            for _ in range(10)
        ]
        mock_result.values = AsyncMock(return_value=expected_records)
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.query_graph(graph_id)

        # Assert
        assert len(result) == 10
        assert result == expected_records


class TestDeleteNode:
    """Тесты для метода delete_node"""

    @pytest.mark.asyncio
    async def test_delete_node_success(self, graph_manager, mock_session, mock_result):
        """Тест успешного удаления узла"""
        # Arrange
        node_id = uuid4()
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.delete_node(node_id)

        # Assert
        assert result is True
        mock_session.run.assert_called_once()
        call_args = mock_session.run.call_args
        assert "DETACH DELETE n" in call_args[0][0]
        assert call_args[1]["node_id"] == node_id

    @pytest.mark.asyncio
    async def test_delete_node_with_zero_id(
        self, graph_manager, mock_session, mock_result
    ):
        """Тест удаления узла с ID 0"""
        # Arrange
        node_id = uuid4()
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.delete_node(node_id)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_node_with_large_id(
        self, graph_manager, mock_session, mock_result
    ):
        """Тест удаления узла с большим ID"""
        # Arrange
        node_id = uuid4()
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.delete_node(node_id)

        # Assert
        assert result is True
        assert mock_session.run.call_args[1]["node_id"] == node_id


class TestDeleteRelationship:
    """Тесты для метода delete_relationship"""

    @pytest.mark.asyncio
    async def test_delete_relationship_success(
        self, graph_manager, mock_session, mock_result
    ):
        """Тест успешного удаления связи"""
        # Arrange
        relationship_id = uuid4()
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.delete_relationship(relationship_id)

        # Assert
        assert result is True
        mock_session.run.assert_called_once()
        call_args = mock_session.run.call_args
        assert "DELETE r" in call_args[0][0]
        assert call_args[1]["relationship_id"] == relationship_id

    @pytest.mark.asyncio
    async def test_delete_relationship_with_zero_id(
        self, graph_manager, mock_session, mock_result
    ):
        """Тест удаления связи с ID 0"""
        # Arrange
        relationship_id = uuid4()
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.delete_relationship(relationship_id)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_relationship_with_large_id(
        self, graph_manager, mock_session, mock_result
    ):
        """Тест удаления связи с большим ID"""
        # Arrange
        relationship_id = uuid4()
        mock_session.run = AsyncMock(return_value=mock_result)

        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(
            return_value=None
        )

        # Act
        result = await graph_manager.delete_relationship(relationship_id)

        # Assert
        assert result is True
        assert mock_session.run.call_args[1]["relationship_id"] == relationship_id
