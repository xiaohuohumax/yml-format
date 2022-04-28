import os
from pathlib import Path

# 基础路径 util 文件存在路径
BASE_PATH: str = os.path.dirname(__file__)


def read_file(file_path: str, mode="r") -> str:
    # 文件读取
    with open(file_path, mode, encoding="utf-8") as file:
        return file.read()


def write_file(file_path: str, data: str, mode="w"):
    # 文件写入
    with open(file_path, mode, encoding="utf-8") as file:
        file.write(data)


def get_abspath(path: str) -> str:
    # 获取项目下的文件绝对路径
    return str(Path(BASE_PATH).joinpath(path))


def path_join(base: str, *join_path) -> str:
    # 路径拼接
    return str(Path(base).joinpath(*join_path))


def delete_dir(path: str):
    # 删除文件夹下的所有文件
    for parent, dirs, fileNames in os.walk(path):
        for name in fileNames:
            file_path = os.path.join(parent, name)
            os.unlink(file_path)
        for dir_path in dirs:
            os.rmdir(dir_path)


def dict_hump(data: any) -> any:
    if isinstance(data, dict):
        # return {re.sub(r'-(\w)', lambda g: g.group(1).upper(), key): dict_hump(data[key]) for key in data.keys()}
        return {key.replace("-", "_"): dict_hump(data[key]) for key in data.keys()}
    elif isinstance(data, list):
        return [dict_hump(item) for item in data]
    else:
        return data
