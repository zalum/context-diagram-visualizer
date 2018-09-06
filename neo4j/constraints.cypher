CREATE CONSTRAINT ON (d:database_user) ASSERT d.system_node_id IS UNIQUE;
CREATE CONSTRAINT ON (t:table) ASSERT t.system_node_id IS UNIQUE;
CREATE CONSTRAINT ON (a:application) ASSERT a.system_node_id IS UNIQUE;
CREATE CONSTRAINT ON (p:product) ASSERT p.system_node_id IS UNIQUE;
