import pytest
from unittest.mock import AsyncMock, MagicMock


class TestAddNode:
    """Тесты для метода add_node"""

    @pytest.mark.asyncio
    async def test_add_node_success(self, graph_manager, mock_session, mock_result):
        """Тест успешного добавления узла"""
        # Arrange
        node_data = {"id": 1, "name": "Test Node", "value": 100}
        mock_record = {"n": {"id": 1, "name": "Test Node", "value": 100}}
        
        mock_result.single = AsyncMock(return_value=mock_record)
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.add_node(node_data)
        
        # Assert
        assert result == mock_record
        mock_session.run.assert_called_once()
        assert "CREATE (n:Node $props)" in mock_session.run.call_args[0][0]

    @pytest.mark.asyncio
    async def test_add_node_empty_data(self, graph_manager, mock_session, mock_result):
        """Тест добавления узла с пустыми данными"""
        # Arrange
        node_data = {}
        mock_result.single = AsyncMock(return_value={})
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.add_node(node_data)
        
        # Assert
        assert result == {}
        mock_session.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_node_with_complex_properties(self, graph_manager, mock_session, mock_result):
        """Тест добавления узла со сложными свойствами"""
        # Arrange
        node_data = {
            "id": 1,
            "name": "Complex Node",
            "metadata": {"type": "test", "version": 1},
            "tags": ["tag1", "tag2"],
        }
        mock_result.single = AsyncMock(return_value=node_data)
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.add_node(node_data)
        
        # Assert
        assert result == node_data
        mock_session.run.assert_called_once_with("CREATE (n:Node $props)", props=node_data)


class TestAddRelationship:
    """Тесты для метода add_relationship"""

    @pytest.mark.asyncio
    async def test_add_relationship_success(self, graph_manager, mock_session, mock_result):
        """Тест успешного добавления связи"""
        # Arrange
        from_id = 1
        to_id = 2
        properties = {"weight": 1.5}
        mock_result.single = AsyncMock(return_value={"r": "relationship"})
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.add_relationship(from_id, to_id, properties)
        
        # Assert
        assert result == {"r": "relationship"}
        mock_session.run.assert_called_once()
        call_args = mock_session.run.call_args
        assert call_args[1]["from_id"] == from_id
        assert call_args[1]["to_id"] == to_id

    @pytest.mark.asyncio
    async def test_add_relationship_without_properties(self, graph_manager, mock_session, mock_result):
        """Тест добавления связи без свойств"""
        # Arrange
        from_id = 1
        to_id = 2
        mock_result.single = AsyncMock(return_value={})
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.add_relationship(from_id, to_id)
        
        # Assert
        assert result == {}
        mock_session.run.assert_called_once()
        call_args = mock_session.run.call_args
        assert call_args[1]["from_id"] == from_id
        assert call_args[1]["to_id"] == to_id

    @pytest.mark.asyncio
    async def test_add_relationship_with_none_properties(self, graph_manager, mock_session, mock_result):
        """Тест добавления связи с None свойствами"""
        # Arrange
        from_id = 1
        to_id = 2
        mock_result.single = AsyncMock(return_value={})
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.add_relationship(from_id, to_id, None)
        
        # Assert
        assert result == {}


class TestQueryGraph:
    """Тесты для метода query_graph"""

    @pytest.mark.asyncio
    async def test_query_graph_success(self, graph_manager, mock_session, mock_result):
        """Тест успешного запроса графа"""
        # Arrange
        graph_id = 1
        expected_records = [
            {"n": {"id": 1, "name": "Node 1"}},
            {"n": {"id": 2, "name": "Node 2"}},
        ]
        mock_result.values = AsyncMock(return_value=expected_records)
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.query_graph(graph_id)
        
        # Assert
        assert result == expected_records
        mock_session.run.assert_called_once()
        assert mock_session.run.call_args[1]["graph_id"] == graph_id

    @pytest.mark.asyncio
    async def test_query_graph_empty_result(self, graph_manager, mock_session, mock_result):
        """Тест запроса графа с пустым результатом"""
        # Arrange
        graph_id = 999
        mock_result.values = AsyncMock(return_value=[])
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.query_graph(graph_id)
        
        # Assert
        assert result == []
        mock_session.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_query_graph_with_multiple_nodes(self, graph_manager, mock_session, mock_result):
        """Тест запроса графа с несколькими узлами"""
        # Arrange
        graph_id = 1
        expected_records = [
            {"n": {"id": i, "name": f"Node {i}", "value": i * 10}}
            for i in range(1, 11)
        ]
        mock_result.values = AsyncMock(return_value=expected_records)
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
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
        node_id = 1
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.delete_node(node_id)
        
        # Assert
        assert result is True
        mock_session.run.assert_called_once()
        call_args = mock_session.run.call_args
        assert "DETACH DELETE n" in call_args[0][0]
        assert call_args[1]["node_id"] == node_id

    @pytest.mark.asyncio
    async def test_delete_node_with_zero_id(self, graph_manager, mock_session, mock_result):
        """Тест удаления узла с ID 0"""
        # Arrange
        node_id = 0
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.delete_node(node_id)
        
        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_node_with_large_id(self, graph_manager, mock_session, mock_result):
        """Тест удаления узла с большим ID"""
        # Arrange
        node_id = 999999
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.delete_node(node_id)
        
        # Assert
        assert result is True
        assert mock_session.run.call_args[1]["node_id"] == node_id


class TestDeleteRelationship:
    """Тесты для метода delete_relationship"""

    @pytest.mark.asyncio
    async def test_delete_relationship_success(self, graph_manager, mock_session, mock_result):
        """Тест успешного удаления связи"""
        # Arrange
        relationship_id = 1
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.delete_relationship(relationship_id)
        
        # Assert
        assert result is True
        mock_session.run.assert_called_once()
        call_args = mock_session.run.call_args
        assert "DELETE r" in call_args[0][0]
        assert call_args[1]["relationship_id"] == relationship_id

    @pytest.mark.asyncio
    async def test_delete_relationship_with_zero_id(self, graph_manager, mock_session, mock_result):
        """Тест удаления связи с ID 0"""
        # Arrange
        relationship_id = 0
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.delete_relationship(relationship_id)
        
        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_relationship_with_large_id(self, graph_manager, mock_session, mock_result):
        """Тест удаления связи с большим ID"""
        # Arrange
        relationship_id = 999999
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        result = await graph_manager.delete_relationship(relationship_id)
        
        # Assert
        assert result is True
        assert mock_session.run.call_args[1]["relationship_id"] == relationship_id


class TestGraphManagerIntegration:
    """Интеграционные тесты для GraphManager"""

    @pytest.mark.asyncio
    async def test_workflow_add_nodes_and_relationship(self, graph_manager, mock_session, mock_result):
        """Тест рабочего процесса: добавление узлов и связи"""
        # Arrange
        node1_data = {"id": 1, "name": "Node 1"}
        node2_data = {"id": 2, "name": "Node 2"}
        
        mock_result.single = AsyncMock(return_value={"n": "created"})
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        node1 = await graph_manager.add_node(node1_data)
        node2 = await graph_manager.add_node(node2_data)
        relationship = await graph_manager.add_relationship(1, 2)
        
        # Assert
        assert node1 == {"n": "created"}
        assert node2 == {"n": "created"}
        assert relationship == {"n": "created"}
        assert mock_session.run.call_count == 3

    @pytest.mark.asyncio
    async def test_workflow_create_and_delete(self, graph_manager, mock_session, mock_result):
        """Тест рабочего процесса: создание и удаление"""
        # Arrange
        node_data = {"id": 1, "name": "Temporary Node"}
        
        mock_result.single = AsyncMock(return_value=node_data)
        mock_session.run = AsyncMock(return_value=mock_result)
        
        graph_manager.driver.session = MagicMock()
        graph_manager.driver.session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        graph_manager.driver.session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Act
        created_node = await graph_manager.add_node(node_data)
        deleted = await graph_manager.delete_node(1)
        
        # Assert
        assert created_node == node_data
        assert deleted is True
