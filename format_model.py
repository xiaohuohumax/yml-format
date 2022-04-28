import uuid
from pathlib import Path

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap

import util
from config import config
from logger import logger


class FormatModel(object):
    # 是否使用相对路径模式
    relative_path_model: bool = True
    # 模块名称 空时默认为包路径
    model_name: str = ""
    # 源文件相对/绝对路径
    from_path: str = ""
    # 目标文件相对/绝对路径
    target_path: str = ""

    # 是否禁用此模块
    disabled: bool = False
    # 模块描述
    describe: str = ""

    # 源文件基础路径
    from_base_path: str = ""
    # 目标文件基础路径
    target_base_path: str = ""

    def __init__(self, from_base_path: str, target_base_path: str):
        if self.relative_path_model:
            self.from_base_path = from_base_path
            self.target_base_path = target_base_path
        self.model_uuid = str(uuid.uuid1().int)
        self.data = None
        if self.model_name == '' or self.model_name is None:
            # 未配置模块名称 则默认为包名
            self.model_name = self.__class__.__module__

    @property
    def from_file(self) -> str:
        # 源文件路径
        return util.path_join(self.from_base_path, self.from_path) if self.relative_path_model else self.from_path

    @property
    def target_file(self) -> str:
        # 目标文件路径
        return util.path_join(self.target_base_path,
                              self.target_path) if self.relative_path_model else self.target_path

    def check(self):
        # 参数校验
        from_file = Path(self.from_file)
        if not from_file.is_file():
            raise Exception(f"源文件不存在 [{self.from_file}]")

        if self.target_file == "":
            raise Exception("目标文件路径为空")

    def format_data(self, root: CommentedMap):
        # 默认格式配置
        logger.info(f"{self.from_file} 已经格式化完成!")

    @property
    def cache_file_path(self) -> str:
        # 获取缓存的yml路径
        return util.path_join(config.yml_format.cache_path, f'{self.model_uuid}.yml')

    def format(self):
        # 格式化处理 并暂时放在缓存目录
        try:
            # 读取源文件
            yml_str = util.read_file(self.from_file)
            yaml = ruamel.yaml.YAML()
            # 读取数据
            self.data = yaml.load(yml_str)
            # 转换
            self.format_data(self.data)
            # 暂存到缓存文件夹中
            with open(self.cache_file_path, mode='w', encoding="utf-8") as file:
                yaml.dump(self.data, file)

        except Exception as e:
            logger.error(f"yml 转换失败 原因: {e}")
            raise e

    def move_to_target(self):
        # 转移到目标文件
        data = util.read_file(self.cache_file_path)
        util.write_file(self.target_file, data)
