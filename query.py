from dashvector import Client


def getQueryUser(queryId):
    client = Client(
        api_key='sk-WnUvx6e64txy8IaGkATNcfeGGa9oJB3DCAF8E129B11EF822C8AC4FB9F1729',
        endpoint='vrs-cn-83l3qpgwq0003e.dashvector.cn-hangzhou.aliyuncs.com'
    )
    collection = client.get(name='USER')
    ret = collection.query(
        id=queryId,
        topk=6,
    )
    # 判断query接口是否成功
    if ret:
        print('query success')
        print(ret)
        # print(len(ret))
        # for doc in ret:
        #     print(doc.id)
        #     print(doc.score)
    return ret
