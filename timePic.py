import pandas as pd
import os
from datetime import datetime, timedelta
from chinese_calendar import is_holiday
from concurrent.futures import ThreadPoolExecutor, as_completed

# 假设的节假日判断函数，这里仅作为示例，实际应用需实现具体逻辑
def isHoliday(date):
    """
    判断给定日期是否为中国节假日。

    参数:
    date (str 或 datetime.date): 需要判断的日期，可以是字符串格式（如"2023-05-01"）或datetime.date对象。

    返回:
    bool: 如果是节假日返回True，否则返回False。
    """
    if isinstance(date, str):
        # 将字符串格式的日期转换为datetime.date对象
        date = datetime.strptime(date, "%Y-%m-%d").date()

    # 使用chinesecalendar库判断是否为节假日
    return is_holiday(date)

# 用户类型判断函数
def user_activity_type(row):
    if row['IsWeekend'] or row['IsHoliday']:
        if row['Active_Period'] in ["上午", "下午"]:
            return "周末活跃型"
        else:
            return "假日休眠型"
    else:
        if row['Active_Period'] == "清晨":
            return "晨鸟型"
        elif row['Active_Period'] in ["上午", "下午"]:
            return "标准工作日型"
        elif row['Active_Period'] == "晚上":
            return "夜猫子型"
        else:
            # 全天候型的判断较为复杂，这里简化处理，实际应用可能需要更精细的规则
            periods = df['Active_Period'].unique()
            if len(periods) == 4 and all(p in periods for p in ["清晨", "上午", "下午", "晚上"]):
                return "全天候型"
            else:
                return "其他"

# 读取 demographic.csv
demographic_path = r'F:\dataAny\orginData\demographic.csv'
demographic_df = pd.read_csv(demographic_path)

# 线程安全的用于更新 dataframe 的函数
def update_demographic_df(user_id, user_type_counts):
    # 确保USERID列是字符串类型，以便正确匹配
    demographic_df['USERID'] = demographic_df['USERID'].astype(str)
    # 更新基础活跃时段分类
    demographic_df.loc[demographic_df['USERID'] == user_id, '基础活跃时段分类'] = str(user_type_counts)

# 处理单个 Excel 文件的函数
def process_file(file_name):
    user_id = file_name.split('.')[0]
    excel_path = os.path.join(folder_path, file_name)
    df = pd.read_excel(excel_path)

    # 确保'T'列是datetime类型
    df['T'] = pd.to_datetime(df['T'], format='%Y-%m-%d %H-%M-%S')

    # 添加活跃时段列
    df['Active_Period'] = df['T'].dt.hour.apply(
        lambda x: "清晨" if 0 <= x < 6
        else "上午" if 6 <= x < 12
        else "下午" if 12 <= x < 18
        else "晚上")

    # 假设有一个'IsWeekend'列来标识是否为周末，这里简单示例，实际情况可能需要更复杂的判断
    df['IsWeekend'] = df['T'].dt.weekday >= 5  # 假设周六周日为周末，0-4为工作日，5-6为周末

    # 添加节假日标识
    df['IsHoliday'] = df['T'].apply(
        lambda x: isHoliday(x.date()) if pd.notnull(x) and 2004 <= x.year <= 2024 else False)

    # 计算用户类型
    df['User_Type'] = df.apply(user_activity_type, axis=1)

    # 只保留前两个最常见的用户类型
    user_type_counts = df['User_Type'].value_counts()[:2]

    # 更新 demographic_df
    update_demographic_df(user_id, user_type_counts)

# 指定 Excel 文件所在的文件夹
folder_path = r'F:\dataAny\output\excel'

# 使用线程池处理所有 Excel 文件
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_file, file_name) for file_name in os.listdir(folder_path) if file_name.endswith('.xlsx')]

# 等待所有任务完成
for future in as_completed(futures):
    future.result
# 保存修改后的 demographic_df 到新的 CSV 文件
output_csv_path = r'F:\dataAny\demographic_with_user_type.csv'
demographic_df.to_csv(output_csv_path, index=False)
print("处理完成，结果已保存到：", output_csv_path)