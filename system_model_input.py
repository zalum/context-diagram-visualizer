def getSystemGraph():
    return {"vertexes":{
            "1":{"name":"precedingapp","type":"application"},
            "2":{"name": "app1","type":"application"},
            "3":{"name":"app2","type":"application"},
            "4":{"name":"app3","type":"application"},
            "5":{"name": "product","type":"product"}
            },
            "edges":[
                {"start":"1","end":"2"},
                {"start":"2","end":"3"},
                {"start":"3","end":"5"},
                {"start":"2","end":"5"},
                {"start":"3","end":"4"},
                {"start":"4","end":"5"}
                ]}

def getDatamodelGraph():
    return {
        "vertexes":{
        "TABLE1":{"type":"table"},
        "TABLE2":{"type":"table"},
        "SCHEMA1":{"type":"schema"},
        "T1_ID":{"type":"column"},
        "T1_PROPERTY1":{"type":"column"},
        "T1_T2_FK":{"type":"column"},
        "T2_ID":{"type":"column"},
        "T2_PROPERTY1":{"type":"column"}
        },
        "edges":[
            {"start":"T1_ID","end":"TABLE1"},
            {"start":"T1_PROPERTY1","end":"TABLE1"},
            {"start":"T1_T2_FK","end":"TABLE1"},
            {"start":"T1_T2_FK","end":"T2_ID"},
            {"start":"T2_ID","end":"TABLE2"},
            {"start":"T2_PROPERTY1","end":"TABLE2"},
            {"start":"TABLE1","end":"SCHEMA1"},
            {"start":"TABLE2","end":"SCHEMA1"},
    ]}
