from dataclasses import dataclass

from ruamel import yaml

import util

# 配置文件路径
file_path = util.get_abspath("./config/application.yml")


@dataclass
class YmlFormat(object):
    from_base_path: str
    target_base_path: str
    log_path: str
    yml_model_path: str
    yml_model_pre: str
    cache_path: str
    banner_path: str

    def __init__(self, from_base_path="/", target_base_path="/", log_path="./config/logger.json",
                 yml_model_path="./yml", yml_model_pre="format", cache_path="./cache",
                 banner_path="./config/banner.txt", *_args, **_keywords):
        self.from_base_path = from_base_path
        self.target_base_path = target_base_path
        self.log_path = util.get_abspath(log_path)
        self.yml_model_path = util.get_abspath(yml_model_path)
        self.yml_model_pre = yml_model_pre
        self.cache_path = util.get_abspath(cache_path)
        self.banner_path = util.get_abspath(banner_path)


@dataclass
class Config(object):
    yml_format: YmlFormat

    def __init__(self, yml_format=None, *_args, **_keywords):
        if yml_format is None:
            yml_format = {}
        self.yml_format = YmlFormat(**yml_format)


config = Config()

try:
    yml = util.read_file(file_path)
    format_yml = util.dict_hump(yaml.safe_load(yml))
    config = Config(**format_yml)
except Exception as e:
    print(f"解析配置文件错误: {file_path} 原因:{e}")
