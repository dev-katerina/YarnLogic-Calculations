from uuid import UUID

from models.neo4j import Stitch, Relation
from repositories.graph_manager import GraphManager
from repositories.db_manager import DBManager

class Patterns():
    def __init__(self, graph_manager: GraphManager, db_manager: DBManager):
        self.graph_manager = graph_manager
        self.db_manager = db_manager

    def create_pattern(self, first_node: Stitch) -> None:
        if not isinstance(first_node, Stitch):
            raise ValueError("first_node должен быть экземпляром класса Stitch")
        if self.db_manager.get_stitch_type_by_name(first_node.stitch_type) is None:
            raise ValueError(
                f"Тип стежка '{first_node.stitch_type}' не найден в базе данных"
            )
        self.graph_manager.add_node(first_node)

    def add_stitch_to_pattern(self, stitch: Stitch, relation: Relation, stitch_id: UUID) -> None:
        if not isinstance(stitch, Stitch):
            raise ValueError("stitch должен быть экземпляром класса Stitch")
        if not isinstance(relation, Relation):
            raise ValueError("relation должен быть экземпляром класса Relation")
        if self.db_manager.get_stitch_type_by_name(stitch.stitch_type) is None:
            raise ValueError(
                f"Тип стежка '{stitch.stitch_type}' не найден в базе данных"
            )
        if self.graph_manager.get_node(stitch_id) is None:
            raise ValueError(f"Стежок с id '{stitch_id}' не найден в графе")
        self.graph_manager.add_node(stitch)
        self.graph_manager.add_relationship(stitch_id, stitch.id, relation)

    def get_pattern(self, graph_id: UUID) -> None:
        if not isinstance(graph_id, UUID):
            raise ValueError("graph_id должен быть экземпляром класса UUID")
        return self.graph_manager.query_graph(graph_id)
    
    def delete_pattern(self, graph_id: UUID) -> None:
        if not isinstance(graph_id, UUID):
            raise ValueError("graph_id должен быть экземпляром класса UUID")
        self.graph_manager.delete_graph(graph_id)
        pass

    def delete_stitch_from_pattern(self, stitch_id: UUID) -> None:
        if not isinstance(stitch_id, UUID):
            raise ValueError("stitch_id должен быть экземпляром класса UUID")
        if self.graph_manager.get_node(stitch_id) is None:
            raise ValueError(f"Стежок с id '{stitch_id}' не найден в графе")
        self.graph_manager.delete_node(stitch_id)
        pass