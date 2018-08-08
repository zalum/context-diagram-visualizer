CREATE CONSTRAINT ON (d:database_user) ASSERT d.system_node_id IS UNIQUE;

CREATE CONSTRAINT ON (d:table) ASSERT d.system_node_id IS UNIQUE