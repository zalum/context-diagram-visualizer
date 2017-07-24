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
