from typing import List
from unittest import result

import pytest
from repositories.graph_manager import GraphManager
from models.neo4j import Stitch, Relation
from db.neo4j import get_driver
from uuid import UUID, uuid4
from repositories.graph_manager import GraphManagerNeo4j

@pytest.mark.parametrize(
    "stitch",
    [
        Stitch(id = uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4())
    ]
)
@pytest.mark.asyncio
async def test_add_node(neo4j_session, stitch):
    graph_manager = GraphManagerNeo4j(neo4j_session)

    await graph_manager.add_node(stitch)

    result = await neo4j_session.run(
        "MATCH (n:Node {id: $node_id}) RETURN n",
        node_id=str(stitch.id)
    )

    record = await result.single()

    assert record is not None
    assert record["n"]["id"] == str(stitch.id)
    assert record["n"]["type"] == stitch.type
    assert record["n"]["tool"] == stitch.tool
    assert record["n"]["graph_id"] == str(stitch.graph_id)

@pytest.mark.parametrize(
    "stitch",
    [
        Stitch(id = uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4() )
    ]
)
@pytest.mark.asyncio
async def test_get_node(neo4j_session, stitch):
    graph_manager = GraphManagerNeo4j(neo4j_session)

    await graph_manager.add_node(stitch)
    node = await graph_manager.get_node(stitch.id)

    assert node.id == stitch.id
    assert node.type == stitch.type
    assert node.tool == stitch.tool
    assert node.graph_id == stitch.graph_id

@pytest.mark.parametrize(
    "stitch",
    [
        Stitch(id = uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4())
    ]
)
@pytest.mark.asyncio
async def test_change_node(neo4j_session, stitch):
    graph_manager = GraphManagerNeo4j(neo4j_session)

    await graph_manager.add_node(stitch)
    stitch.type = "updated_stitch"
    await graph_manager.change_node(stitch)
    node = await graph_manager.get_node(stitch.id)

    assert node.id == stitch.id
    assert node.type == stitch.type
    assert node.tool == stitch.tool
    assert node.graph_id == stitch.graph_id

@pytest.mark.parametrize(
    "stitch1, stitch2, relation_data",
    [
        (
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4()),
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4()),
            Relation(id=uuid4(), type="relation", graph_id=uuid4())
        )
    ]
)
@pytest.mark.asyncio
async def test_add_relationship(neo4j_session, stitch1, stitch2, relation_data):
    graph_manager = GraphManagerNeo4j(neo4j_session)

    await graph_manager.add_node(stitch1)
    await graph_manager.add_node(stitch2)
    await graph_manager.add_relationship(stitch1.id, stitch2.id, relation_data)

    result = await neo4j_session.run(
        "MATCH (n:Node {id: $from_id})-[r]->(m:Node {id: $to_id}) RETURN r",
        from_id=str(stitch1.id),
        to_id=str(stitch2.id)
    )

    record = await result.single()

    assert record is not None
    assert record["r"]["id"] == str(relation_data.id)
    assert record["r"]["type"] == relation_data.type
    assert record["r"]["graph_id"] == str(relation_data.graph_id)

@pytest.mark.parametrize(
    "stitch1, stitch2, relation_data",
    [
        (
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4()),
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4()),
            Relation(id=uuid4(), type="relation", graph_id=uuid4())
        )
    ]
)
@pytest.mark.asyncio
async def test_change_relationship(neo4j_session, stitch1, stitch2, relation_data):
    graph_manager = GraphManagerNeo4j(neo4j_session)

    await graph_manager.add_node(stitch1)
    await graph_manager.add_node(stitch2)

    await graph_manager.add_relationship(stitch1.id, stitch2.id, relation_data)
    relation_data.type = "updated_relation"
    await graph_manager.change_relationship(stitch1.id, stitch2.id, relation_data)

    result = await neo4j_session.run(
        "MATCH (n:Node {id: $from_id})-[r]->(m:Node {id: $to_id}) RETURN r",
        from_id=str(stitch1.id),
        to_id=str(stitch2.id)
    )

    record = await result.single()

    assert record is not None
    assert record["r"]["id"] == str(relation_data.id)
    assert record["r"]["type"] == relation_data.type
    assert record["r"]["graph_id"] == str(relation_data.graph_id)

@pytest.mark.parametrize(
    "graph_id,stitch1, stitch2, relation_data",
    [
        (
            graph_id := uuid4(),
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=graph_id),
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=graph_id),
            Relation(id=uuid4(), type="relation", graph_id=graph_id)
        )
    ]
)
@pytest.mark.asyncio
async def test_query_graph(neo4j_session, graph_id, stitch1, stitch2, relation_data):
    graph_manager = GraphManagerNeo4j(neo4j_session)

    await graph_manager.add_node(stitch1)
    await graph_manager.add_node(stitch2)

    await graph_manager.add_relationship(stitch1.id, stitch2.id, relation_data)
    items = await graph_manager.query_graph(graph_id)

    assert len(items) == 1
    assert isinstance(items[0][0], Stitch)
    assert isinstance(items[0][1], Relation)
    assert isinstance(items[0][2], Stitch)
    assert items[0][1].id == relation_data.id


@pytest.mark.parametrize(
    "stitch",
    [
        Stitch(id = uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4())
    ]
)
@pytest.mark.asyncio
async def test_delete_node(neo4j_session, stitch):
    graph_manager = GraphManagerNeo4j(neo4j_session)

    await graph_manager.add_node(stitch)
    await graph_manager.delete_node(stitch.id)

    result = await neo4j_session.run(
        "MATCH (n:Node {id: $node_id}) RETURN n",
        node_id=str(stitch.id)
    )
    record = await result.single()
    assert record is None

@pytest.mark.parametrize(
    "stitch1, stitch2, relation_data",
    [
        (
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4()),
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=uuid4()),
            Relation(id=uuid4(), type="relation", graph_id=uuid4())
        )
    ]
)
@pytest.mark.asyncio
async def test_delete_relationship(neo4j_session, stitch1, stitch2, relation_data):
    graph_manager = GraphManagerNeo4j(neo4j_session)
    await graph_manager.add_node(stitch1)
    await graph_manager.add_node(stitch2)
    await graph_manager.add_relationship(stitch1.id, stitch2.id, relation_data)
    await graph_manager.delete_relationship(relation_data.id)

    result = await neo4j_session.run(
        "MATCH ()-[r:RELATION {id: $relationship_id}]-() RETURN r",
        relationship_id=str(relation_data.id)
    )
    record = await result.single()
    assert record is None

@pytest.mark.parametrize(
    "graph_id,stitch1, stitch2, relation_data",
    [
        (
            graph_id := uuid4(),
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=graph_id),
            Stitch(id=uuid4(), type="stitch", tool="Test Tool", graph_id=graph_id),
            Relation(id=uuid4(), type="relation", graph_id=graph_id)
        )
    ]
)
@pytest.mark.asyncio
async def test_delete_graph(neo4j_session, graph_id, stitch1, stitch2, relation_data):
    graph_manager = GraphManagerNeo4j(neo4j_session)

    await graph_manager.add_node(stitch1)
    await graph_manager.add_node(stitch2)

    await graph_manager.add_relationship(stitch1.id, stitch2.id, relation_data)
    await graph_manager.delete_graph(graph_id)

    count_result = await neo4j_session.run(
        """
        MATCH (n:Node {graph_id: $graph_id})-[r:RELATION]->(m:Node)
        RETURN COUNT(*) as cnt
        """,
        graph_id=str(graph_id)
    )
    record = await count_result.single()
    assert record["cnt"] == 0