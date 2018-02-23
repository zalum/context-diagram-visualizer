from smv import system_model_visualizer as smv, system_model_output as smo
from smv.core.model import system_model as sm


def get_datamodel_graph():
    return {
        "system-nodes":{
        "TABLE1":{"type":"table"},
        "TABLE2":{"type":"table"},
        "SCHEMA1":{"type":"schema"},
        "T1_ID":{"type":"column"},
        "T1_PROPERTY1":{"type":"column"},
        "T1_T2_FK":{"type":"column"},
        "T2_ID":{"type":"column"},
        "T2_PROPERTY1":{"type":"column"}
        },
        "relations":[
            {"start":"T1_ID","end":"TABLE1"},
            {"start":"T1_PROPERTY1","end":"TABLE1"},
            {"start":"T1_T2_FK","end":"TABLE1"},
            {"start":"T1_T2_FK","end":"T2_ID","relation_type":"fk"},
            {"start":"T2_ID","end":"TABLE2"},
            {"start":"T2_PROPERTY1","end":"TABLE2"},
            {"start":"TABLE1","end":"SCHEMA1"},
            {"start":"TABLE2","end":"SCHEMA1"},
    ]}


def get_dynamo_datamodel_graph():
    datamodel = {
  "system-nodes":{
      "ns_order-export-prod":{"type":"database-user"},
      "order-export-prod_PurchaseOrderEvents":{"type":"table"},
      "order-export-prod_PurchaseOrderEvents_Positions":{"type":"table"},
      "key":{"type":"column"},
      "timestamp":{"type":"column"},
      "purchaseOrderEventType":{"type":"column"},
      "purchaseOrderId":{"type":"column"},
      "articleSupplierId":{"type":"column"}
  },
  "relations":[
      {"start":"ns_order-export-prod","end":"order-export-prod_PurchaseOrderEvents","relation_type":"contains"},
      {"start":"ns_order-export-prod","end":"order-export-prod_PurchaseOrderEvents_Positions","relation_type":"contains"},
      {"start":"order-export-prod_PurchaseOrderEvents","end":"key","relation_type":"contains"},
      {"start":"order-export-prod_PurchaseOrderEvents","end":"timestamp","relation_type":"contains"},
      {"start":"order-export-prod_PurchaseOrderEvents","end":"purchaseOrderEventType","relation_type":"contains"},
      {"start":"order-export-prod_PurchaseOrderEvents","end":"purchaseOrderId","relation_type":"contains"},
      {"start":"order-export-prod_PurchaseOrderEvents_Positions","end":"articleSupplierId","relation_type":"contains"},
      {"start":"order-export-prod_PurchaseOrderEvents_Positions",
       "end":"order-export-prod_PurchaseOrderEvents",
       "relation_type":"composition"}
  ]
}

    return datamodel


def draw_datamodel():
    f = open('output-dm.png', 'wb')
    inputSystemGraph = sm.data_model(get_dynamo_datamodel_graph())
    lines = smv.datamodel_visualizer(inputSystemGraph).draw(colapsed_columns=False)
    picture = smo.writeAsImage(lines).getvalue()
    f.write(picture)


draw_datamodel()