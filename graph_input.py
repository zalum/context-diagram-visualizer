def getSystemGraph():
    return {"vertexes":[
            {"name":"precedingapp","key":"1","type":"application"},
            {"name": "app1","key":"2","type":"application"},
            {"name":"app2","key":"3","type":"application"},
            {"name":"app3","key":"4","type":"application"},
            {"name": "product","key":"5","type":"product"}],
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
        "vertexes":[
        {"key":"TABLE1","type":"table"},
        {"key":"TABLE2","type":"table"},
        {"key":"SCHEMA1","type":"schema"},
        {"key":"T1_ID","type":"column"},
        {"key":"T1_PROPERTY1","type":"column"},
        {"key":"T1_T2_FK","type":"column"},
        {"key":"T2_ID","type":"column"},
        {"key":"T2_PROPERTY1","type":"column"}
    ],
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
