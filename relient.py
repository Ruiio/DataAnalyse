import pandas as pd
from collections import Counter
from openai import OpenAI
import os
from concurrent.futures import ThreadPoolExecutor

# 定义文件夹路径
folder_path = r'F:\dataAny\output\excel'

# 创建一个空的DataFrame来存储所有文件的处理结果
results_df = pd.DataFrame(columns=['文件名', '处理所得的fstr', '模型所给的响应'])

# 定义API keys列表
api_keys = [
    "sk-532985b0b318440cbc097b53ac40e491",
    "sk-3699ea9adddd4c1aa534b8c91de67ef0",
    "sk-aa2a5ad563854c9093f40fc7c6f31f4a"
]

# 定义处理文件的函数
def process_file(filename, api_keys):
    file_path = os.path.join(folder_path, filename)
    try:
        # 读取Excel文件
        data = pd.read_excel(file_path)

        # 准备一个列表来存储所有出现的程序名称
        program_names = []

        # 遍历数据集中的每条记录，提取程序名称
        for index, row in data.iterrows():
            # 假设N字段是'ProgramName'，P字段是'ProcessName'
            try:
                program_name = row['N'] if pd.notnull(row['N']) else row['P']
                program_names.append(program_name)
            except KeyError:
                # 如果列名不存在，捕获KeyError并跳过当前行
                continue

        # 使用Counter来统计程序名称的出现次数
        program_counts = Counter(program_names)

        # 定义一个阈值，用于确定哪些应用程序是“频繁使用”的
        threshold = 10  # 例如，出现次数超过10次的应用程序被认为是核心应用程序

        # 提取频繁使用的核心应用程序
        core_programs = {program: count for program, count in program_counts.items() if count > threshold}

        # 生成fstr字符串
        fstr = ""
        for program, count in core_programs.items():
            fstr = fstr + "\n" + f"{program}: {count}次"

        # 调用OpenAI API获取响应
        for api_key in api_keys:
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                prompt = f"""
                    "请根据用户的软件使用行为，推测用户类型、给出用户类型标签，并解释其原因。
                    请使用以下格式输出你的回答：
                    用户类别标签：XXX,XXX,XXX[end]
                    标签解释：1.XXXXXXXXXX。
                             2.XXXXXXXXXX。
                             3.XXXXXXXXXX。

                下面是用户使用软件频次：
                    {fstr}
                """
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ]
                )
                print(fstr)
                print(response.choices[0].message.content)
                # 返回处理结果
                return {'文件名': filename, '处理所得的fstr': fstr, '模型所给的响应': response.choices[0].message.content}
            except Exception as e:
                print(f"使用API key {api_key} 时出现错误: {e}")
        # 如果所有API keys都失败，则返回错误信息
        return {'文件名': filename, '处理所得的fstr': 'error', '模型所给的响应': 'error'}
    except Exception as e:
        # 如果读取文件或处理数据时出现任何错误，捕获异常并记录错误信息
        print(f"处理文件 {filename} 时出现错误: {e}")
        return {'文件名': filename, '处理所得的fstr': 'error', '模型所给的响应': 'error'}


# 使用多线程处理文件
with ThreadPoolExecutor() as executor:
    # 使用多线程处理文件
    with ThreadPoolExecutor() as executor:
        # 获取所有Excel文件的列表并排序
        excel_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.xlsx')])

        # 从第251个文件开始处理
        excel_files = excel_files[250:]

        # 提交任务
        futures = [executor.submit(process_file, filename, api_keys) for filename in excel_files]

        # 收集结果
        for future in futures:
            results_df = results_df.append(future.result(), ignore_index=True)

    # 将结果保存到新的Excel文件中
    output_file_path = r'F:\dataAny\output\results2.xlsx'
    results_df.to_excel(output_file_path, index=False)
