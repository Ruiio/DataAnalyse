import dashscope
import pandas as pd
from dashscope import TextEmbedding
from dashvector import Client
from typing import List, Union


dashscope.api_key = 'sk-9cf446617c394bbf9f1d0c0f994efff9'


# 调用DashScope通用文本向量模型，将文本embedding为向量
def generate_embeddings(texts: Union[List[str], str], text_type: str = 'document'):
    try:
        rsp = TextEmbedding.call(
            model=TextEmbedding.Models.text_embedding_v2,
            input=texts,
            text_type=text_type
        )
        # 检查rsp对象是否有output键，并且output['embeddings']不是None
        if rsp.output and rsp.output.get('embeddings'):
            embeddings = [record['embedding'] for record in rsp.output['embeddings']]
            return embeddings if isinstance(texts, list) else embeddings[0]
        else:
            print("No embeddings found in rsp.output")
            return None
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None


# 创建DashVector Client
client = Client(
    api_key='sk-WnUvx6e64txy8IaGkATNcfeGGa9oJB3DCAF8E129B11EF822C8AC4FB9F1729',
    endpoint='vrs-cn-83l3qpgwq0003e.dashvector.cn-hangzhou.aliyuncs.com'
)


collection = client.get('USER')
assert collection
file_path = r'F:\下载\article\merged_data_outer (3).xlsx'  # Update with the actual file path
data = pd.read_excel(file_path)

# 第一列将作为唯一标识符
for index, row in data.iterrows():
    identifier = row.iloc[0]  # 第一列作为唯一标识符
    row_string = ' '.join(row.iloc[1:].astype(str))  # 将除第一列之外的所有列的数据转换为字符串并拼接
    print(index)
    print(row_string)
    # 生成嵌入
    if row_string:
        embeddings = generate_embeddings(row_string)
        # 向量入库DashVector
        collection.insert(
            (identifier, embeddings)
        )


