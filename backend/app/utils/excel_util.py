import pandas as pd
import os
from datetime import datetime

# Excel导出工具
def export_user_excel(data_list, save_path):
    format_data = []
    for item in data_list:
        format_data.append({
            "用户ID": item["id"],
            "用户名": item["username"],
            "用户昵称": item["nickname"],
            "创建时间": item["create_time"]
        })
    df = pd.DataFrame(format_data)
    df.to_excel(save_path, index=False, engine="openpyxl")
    return save_path

# Excel导入解析工具
def import_user_excel(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")
    df = df.dropna(subset=["用户名"])
    return df.to_dict(orient="records")
