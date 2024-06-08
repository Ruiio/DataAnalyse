import os
from multiprocessing import Pool

import pandas as pd
from datetime import datetime, timedelta

behavior_folder = r"F:\dataAny\orginData\behavior"
output_folder = r"output\excel"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def parse_start_time(start_time_str):
    return datetime.strptime(start_time_str.replace('<=>', '').replace('L_Start','').strip(), "%Y-%m-%d %H-%M-%S")

def parse_line(line, start_time):
    parts = line.split("[=]")
    data = {part.split("<=>")[0].strip("<=>"): part.split("<=>")[-1].strip("<=>") for part in parts if "<=>" in part}
    if 'T' in data:
        t_seconds = int(data['T'])
        data['T'] = (start_time + timedelta(seconds=t_seconds)).strftime("%Y-%m-%d %H-%M-%S")
    return data

def process_file(file_path):
    """
    处理单个文件并将数据追加写入Excel。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    L_Start = parse_start_time(lines[1])
    new_data = [parse_line(line, L_Start) for line in lines[2:]]
    user_id = os.path.basename(file_path).split("_")[0]
    output_file = os.path.join(output_folder, f"{user_id}.xlsx")

    try:
        existing_df = pd.read_excel(output_file)
    except FileNotFoundError:
        existing_df = pd.DataFrame()

    new_df = pd.DataFrame(new_data)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df.to_excel(output_file, index=False)

    print(f"Excel文件 {output_file} 追加写入完成。")

if __name__ == "__main__":
    behavior_folder = r"F:\dataAny\orginData\behavior"
    output_folder = "output"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取所有.txt文件的完整路径
    txt_files = [os.path.join(root, file) for root, dirs, files in os.walk(behavior_folder) for file in files if file.endswith(".txt")]

    # 使用多进程处理文件
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(process_file, txt_files)

    print("所有Excel文件多进程处理完成。")