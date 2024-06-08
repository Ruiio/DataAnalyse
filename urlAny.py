import pandas as pd
import os
from openai import OpenAI
import threading

api_keys = [
    "sk-532985b0b318440cbc097b53ac40e491",
    "sk-3699ea9adddd4c1aa534b8c91de67ef0",
    "sk-aa2a5ad563854c9093f40fc7c6f31f4a"
]
import queue

# 文件夹路径，请根据实际情况修改
folder_path = r'F:\dataAny\output\excel'

# 创建一个队列来存储每个线程的处理结果
result_queue = queue.Queue()


# 定义处理文件的函数
def process_file(api_keys, file_path, result_queue):
    try:
        # 由于我们不知道确切的文件类型，这里假设它是.xlsx格式
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"加载文件 {file_path} 时出错:", str(e))
        return

    # 检查DataFrame是否成功加载，并且包含“U”列
    if 'U' in df.columns:
        # 统计“U”列中各个值的数量
        u_counts = df['U'].value_counts()
        print(u_counts)
        # 如果U列只有about:blank，则不调用API
        if len(u_counts) == 1 and u_counts.index[0] == 'about:blank':
            print(f"文件 {file_path} 中'U'字段只包含'about:blank'，跳过API调用。")
            result_queue.put({
                'filename': os.path.basename(file_path),
                'urlCount': u_counts.sum(),
                'Response': "跳过API调用"
            })
            return

        response = ""
        for api_key in api_keys:
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                prompt = f"""
                                    "请根据用户的网址访问记录，判断用户类别并做一个用户行为分析：
                                    请使用以下格式输出你的回答：
                                        用户类别：
                                        用户行为分析：
                                下面是用户使用网页访问记录：
                                    {u_counts}
                                """
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ]
                )
                print(u_counts)
                print(response.choices[0].message.content)
                break
            except Exception as e:
                # 如果读取文件或处理数据时出现任何错误，捕获异常并记录错误信息
                print(f"响应时出现错误: {e},切换api")
                continue

        # 获取文件名
        filename = os.path.basename(file_path)

        # 将结果放入队列
        result_queue.put({
            'filename': filename,
            'urlCount': u_counts,
            'Response': response.choices[0].message.content if response else "API响应失败"
        })

    else:
        print(f"文件 {file_path} 没有找到'U'字段。")


# 遍历文件夹中的所有Excel文件
threads = []
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        # 创建线程处理文件
        thread = threading.Thread(target=process_file, args=(api_keys, file_path, result_queue))
        thread.start()
        threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()

# 从队列中取出所有结果并构建DataFrame
global_df = pd.DataFrame(columns=['filename', 'urlCount', 'Response'])
while not result_queue.empty():
    global_df = global_df.append(result_queue.get(), ignore_index=True)

# 将全局DataFrame写入新的Excel文件
output_file_path = os.path.join(folder_path, r'F:\dataAny\combine\processed_data.xlsx')
global_df.to_excel(output_file_path, index=False)

print("所有文件处理完成，结果已保存到：", output_file_path)
