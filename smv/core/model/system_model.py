import json
import logging
from sms import nodes
from sms import relations
from sms.generic_types import Relation

from smv.core import Response
from smv.core import RESPONSE_OK
from smv.core import RESPONSE_ERROR


def empty_graph():
    return {SYSTEM_NODES: {}, RELATIONS: []}


SYSTEM_NODES = "system-nodes"
RELATIONS = "relations"
SYSTEM_NODE_TYPE = "type"
RELATION_TYPE = "relation_type"


class Instrumentation:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def node_type_does_not_exist(self, key, type):
        self.__logger.warn("Node type '{}' of node {} does not exist".format(type, key))

    def relation_type_does_not_exist(self, relation_type, from_type=None, to_type=None):
        self.__logger.warn(
            "Relation type ('{}') from ('{}') to ('{}') does not exist".format(relation_type, from_type, to_type))


instrumentation = Instrumentation()


class DatamodelRelationTypes:
    uses = "uses"


class system_model:
    def __init__(self, graphx=None):
        if graphx is None or len(graphx.keys()) == 0:
            self.graph = empty_graph()
        else:
            self.graph = graphx

    def __str__(self):
        return json.dumps(self.graph, indent=2)

    def get_system_node(self, system_node):
        if system_node not in self.graph[SYSTEM_NODES]:
            return None
        return self.graph[SYSTEM_NODES][system_node]

    def get_system_nodes(self):
        keys = list(self.graph[SYSTEM_NODES].keys())
        keys.sort()
        return keys

    def get_system_nodes_of_type(self, type)->[]:
        return [v for v in self.get_system_nodes() if self.is_system_node_of_type(v, type)]

    def has_system_node(self, system_node):
        return system_node in self.graph[SYSTEM_NODES]

    def get_relations(self):
        return self.graph[RELATIONS] if RELATIONS in self.graph else []

    @staticmethod
    def is_relation_of_type(edge, relation_type):
        if relation_type is None and RELATION_TYPE not in edge:
            return True
        if RELATION_TYPE in edge and edge[RELATION_TYPE] == relation_type:
            return True
        return False

    def get_relations_of_type(self, relation_type):
        return [e for e in self.get_relations() if system_model.is_relation_of_type(e, relation_type)]

    def is_system_node_of_type(self, system_node, type):
        return self.graph[SYSTEM_NODES][system_node]["type"] == type

    def add_system_node(self, key, type, **kwargs):
        if nodes.get_value(type) is None:
            instrumentation.node_type_does_not_exist(key, type)
        if key in self.graph[SYSTEM_NODES]:
            return Response.error("System Node '{}' already exists".format(key))
        self.graph[SYSTEM_NODES][key] = kwargs
        self.graph[SYSTEM_NODES][key]["type"] = type
        return Response.success({key: self.get_system_node(key)})

    def add_relation(self, start, end, relation_type=None, partial_append=False):
        if partial_append is False:
            if self.get_system_node(start) is None:
                return Response.error("Start node '{}' is not in the model".format(start))
            if self.get_system_node(end) is None:
                return Response.error("End node '{}' is not in the model".format(end))
        result = self.get_relation(start=start, end=end, relation_type=relation_type)
        if result.return_code == RESPONSE_OK:
            return Response.error("edge already exists")
        if result.content == "not found":
            self.__verify_relation_type(start, end, relation_type)
            result = {"start": start, "end": end}
            if relation_type is not None:
                result[RELATION_TYPE] = relation_type
            self.graph[RELATIONS].append(result)
            return Response.success("Relation ({})-[{}]-({}) added".format(start, relation_type, end))
        return Response.error(result.content)

    @staticmethod
    def get_relation_type(relation):
        return relation[RELATION_TYPE]

    @staticmethod
    def get_related_system_node(system_node, edge):
        return edge["start"] if edge["end"] == system_node else edge["end"]

    def get_relations_of_system_node(self, with_system_node):
        return list(filter(lambda edge: with_system_node in (edge["start"], edge["end"]), self.get_relations()))

    def get_children(self, parent_system_node, of_type=None, in_relation_of=None):
        return list(
            filter(lambda child: of_type is None or self.is_system_node_of_type(child, of_type),
                   map(lambda edge: self.get_related_system_node(parent_system_node, edge),
                       filter(lambda edge: in_relation_of is None or
                                           system_model.is_relation_of_type(edge, in_relation_of),
                              self.get_relations_of_system_node(parent_system_node)))))

    def copy_system_node(self, from_model: 'system_model', system_node):
        vertex_value = dict(from_model.get_system_node(system_node))
        type = vertex_value.pop("type")
        self.add_system_node(system_node, type, **vertex_value)

    def _is_system_node_in_relations(self, system_node):
        for edge in self.get_relations():
            if self._is_relation_with_system_node(edge, system_node):
                return True
        return False

    def _is_relation_with_system_node(self, relation, system_node):
        return relation["start"] == system_node or relation["end"] == system_node

    def get_orphan_system_nodes(self, ofType):
        return [v for v in self.get_system_nodes_of_type(ofType) if not self._is_system_node_in_relations(v)]

    def set_model(self, new_model: 'system_model'):
        self.graph = empty_graph()
        self.append(new_model)

    def append(self, to_append: 'system_model', partial_append=False):
        for vertex in to_append.graph[SYSTEM_NODES]:
            self.add_system_node(vertex, **to_append.graph[SYSTEM_NODES][vertex])
        for edge in to_append.graph[RELATIONS]:
            self.add_relation(edge["start"], edge["end"], edge[RELATION_TYPE] if RELATION_TYPE in edge else None,
                              partial_append)

    def get_relation(self, start, end, relation_type):
        edges = list(
            filter(lambda edge: system_model.is_relation_of_type(edge, relation_type),
                   filter(lambda edge: start == edge["start"] and end == edge["end"], self.get_relations())))
        if edges is None or len(edges) == 0:
            return Response.error("not found")
        if len(edges) > 1:
            return Response.error("more then one edge ({}) found for (start={} end={} relation_type={})". \
                                  format(len(edges), start, end, relation_type))
        return Response.success(edges[0])

    def remove_relation(self, start, end, relation_type):
        result = self.get_relation(start, end, relation_type)
        if result.return_code == RESPONSE_ERROR:
            return result
        self.graph[RELATIONS].remove(result.content)
        return Response.success()

    def get_relation_types_between(self, node1, node2):
        all_relations = self.get_relations_of_system_node(node1)
        relation_types = set()
        for relation in all_relations:
            if system_model.get_related_system_node(node1, relation) != node2:
                continue
            relation_type = system_model.get_relation_type(relation)
            relation_types.add(relation_type)
        return relation_types

    def __verify_relation_type(self, start, end, relation_type):
        if relation_type is None:
            return
        from_node = self.get_system_node(start)
        to_node = self.get_system_node(end)
        if from_node is None or to_node is None:
            return
        relation = relations.get_value(relation_type)  # type: Relation
        if relation is None:
            instrumentation.relation_type_does_not_exist(relation_type)
            return
        from_type = from_node[SYSTEM_NODE_TYPE]
        to_type = to_node[SYSTEM_NODE_TYPE]
        if not relation.supports(from_type=from_type, to_type=to_type):
            instrumentation.relation_type_does_not_exist(relation_type, from_type=from_type, to_type=to_type)


class component_model(system_model):
    def get_calling_relations(self):
        return self.get_relations_of_type("calls")

    def get_orphan_applications(self):
        return self.get_orphan_system_nodes("application")

    def is_product(self, system_node):
        return self.is_system_node_of_type(system_node, "product")

    def get_component_name(self, system_node):
        if "name" in self.graph[SYSTEM_NODES][system_node]:
            return self.graph[SYSTEM_NODES][system_node]["name"]
        return system_node

    def get_applications_in_product(self, product):
        return self.get_children(product, of_type="application", in_relation_of="contains")

    def getProducts(self):
        return self.get_system_nodes_of_type("product")


class data_model(system_model):
    def add_databse_user(self, database_user):
        self.add_system_node(database_user, nodes.database_user)

    def add_column(self, column, table, owner):
        table_id = self.__build_table_id(owner, table)
        response = self.add_system_node(column, nodes.column)
        if response.is_error():
            return response
        response = self.add_relation(column, table_id, relations.contains)
        return response

    def add_used_table(self, table, owner, database_user, relation: Relation):
        table_id = self.__build_table_id(owner, table)
        if self.get_system_node(table_id) is None:
            self.add_owned_table(table, owner)
        self.add_relation(table_id, database_user, relation)

    def add_owned_table(self, table, owner):
        table_id = self.__build_table_id(owner, table)
        self.add_system_node(table_id, nodes.table, name=table)
        self.add_relation(table_id, owner, relations.contains)

    @staticmethod
    def __build_table_id(owner, table):
        return "{}.{}".format(owner, table)

    def is_table(self, system_node):
        return self.is_system_node_of_type(system_node, nodes.table)

    def get_table_for_column(self, column):
        column_edges = [edge for edge in self.get_relations_of_type(relation_type=relations.contains)
                        if column in (edge["start"], edge["end"])]
        for edge in column_edges:
            system_node = self.get_related_system_node(column, edge)
            if self.is_table(system_node):
                return system_node
        return None

    def get_database_users(self):
        return self.get_system_nodes_of_type(nodes.database_user)

    def get_tables_in_database_user(self, database_user):
        return self.get_children(database_user, nodes.table, relations.contains)

    def get_columns_in_table(self, table):
        return self.get_children(table, nodes.column, in_relation_of=relations.contains)

    def get_foreign_keys(self):
        return list(
            map(lambda fk: self._get_foreign_key(fk["start"], fk["end"]),
                self.get_relations_of_type(relations.foreign_key)))

    def _get_foreign_key(self, column1, column2):
        return {
            "start": {
                "column": column1,
                "table": self.get_table_for_column(column1)
            },
            "end": {
                "column": column2,
                "table": self.get_table_for_column(column2)
            }
        }

