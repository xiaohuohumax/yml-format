import argparse
import importlib
import os
import time

import util
from config import config
from format_model import FormatModel
from logger import logger


class Format(object):
    _models: list = []
    # 运行前后是否删除缓存
    _clear_cache: bool = True
    # 显示 banner
    _allow_show_banner: bool = True
    # 是否允许 args 修改配置
    _allow_params: bool = True

    def __init__(self):
        # from_base_path 源文件基础路径 target_base_path 目标基础路径
        self._show_banner()
        self._init_params()
        self._clear_cache_file()
        self._load_model()
        self._model_check()
        self._format()
        self._move_to_target()
        self._clear_cache_file()

    def _load_model(self):
        # 加载模块 yml 文件夹下的所有文件
        logger.info("开始加载模块")
        for parent, _, fileNames in os.walk(config.yml_format.yml_model_path):
            for name in fileNames:
                if (name.startswith(config.yml_format.yml_model_pre)) and name.endswith('.py'):
                    # 包名
                    package = "{}.{}".format(parent.replace(util.BASE_PATH + '\\', '').replace('\\', '.'), name[:-3])
                    try:
                        model = importlib.import_module(package)
                        item = model.FormatModelItem(config.yml_format.from_base_path,
                                                     config.yml_format.target_base_path)
                        if not isinstance(item, FormatModel):
                            raise Exception("模块未继承 FormatModel")
                        if item.disabled:
                            logger.info(f"模块放弃加载[{item.model_name}]")
                            continue
                        self._models.append(item)
                        logger.info(f"成功加载模块[{item.model_name}] {item.describe}")
                    except AttributeError as e:
                        logger.error(f"加载初始化失败: {package} 原因: {e}")
                        raise e
        model_name = [item.model_name for item in self._models]
        logger.info(f"成功加载{len(model_name)}个模块{model_name}")

    def _model_check(self):
        logger.info("开始检查模块参数是否正确")
        for item in self._models:
            try:
                if isinstance(item, FormatModel):
                    item.check()
                    logger.info(f"模块[{item.model_name}]参数校验成功")
            except Exception as e:
                logger.error(f"模块[{item.model_name}]参数校验失败 原因: {e}")
                raise e

    def _format(self):
        logger.info("开始配置文件转换")
        # 开始格式化
        for item in self._models:
            if isinstance(item, FormatModel):
                try:
                    item.format()
                    logger.info(f"模块[{item.model_name}]格式化成功,已暂存至[{item.cache_file_path}]")
                except Exception as e:
                    logger.error(f"模块[{item.model_name}]格式化错误 原因: {e}")
                    raise e

    def _clear_cache_file(self):
        # 清除缓存文件夹
        if self._clear_cache:
            util.delete_dir(config.yml_format.cache_path)
            logger.info("缓存文件已清除")

    def _move_to_target(self):
        logger.info("开始将配置文件转移到目标地址")
        # 开始移动配置文件
        for item in self._models:
            if isinstance(item, FormatModel):
                try:
                    item.move_to_target()
                    logger.info(f"移动配置文件成功 [{item.cache_file_path}] => [{item.target_file}]")
                except Exception as e:
                    logger.error(f"模块[{item.model_name}] 格式化 [{item.cache_file_path}] 结果移动错误 原因: {e}")
                    raise e

        targets = [item.target_file for item in self._models]
        logger.info(f"已完成{len(targets)}个配置文件转移到目标地址{targets}")

    def _init_params(self):
        if self._allow_params:
            # 参数传入格式
            # python main.py  -t "目标基础路径" -f "源基础路径" -m "模块前缀"
            # 配置基础路径
            parser = argparse.ArgumentParser("python main.py")
            # 参数缺失时 路径默认为 配置文件配置
            parser.add_argument("-t", default=config.yml_format.target_base_path, type=str,
                                help=f"目标基础路径,默认:{config.yml_format.target_base_path}")
            parser.add_argument("-f", default=config.yml_format.from_base_path, type=str,
                                help=f"源基础路径,默认:{config.yml_format.from_base_path}")
            parser.add_argument("-m", default=config.yml_format.yml_model_pre, type=str,
                                help=f"模块前缀,默认:{config.yml_format.yml_model_pre}")
            args = parser.parse_args()

            config.yml_format.target_base_path = args.t
            config.yml_format.from_base_path = args.f
            config.yml_format.yml_model_pre = args.m

            logger.info(f"源基础路径:{config.yml_format.from_base_path}")
            logger.info(f"目标基础路径:{config.yml_format.target_base_path}")
            logger.info(f"模块前缀:{config.yml_format.yml_model_pre}")

    def _show_banner(self):
        if self._allow_show_banner:
            try:
                print(util.read_file(config.yml_format.banner_path))
                time.sleep(0.125)
            except Exception as e:
                logger.warn("加载 banner 错误", e)
