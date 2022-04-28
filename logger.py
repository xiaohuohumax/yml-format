import json
import logging
import logging.config

import util
from config import config


def Logger(logger_path):
    try:
        _logger = logging.getLogger()
        logger_str = util.read_file(logger_path)
        logging.config.dictConfig(json.loads(logger_str))
        return _logger
    except Exception as e:
        print(f'logger 初始化错误 原因: {e}')


# 日志
logger = Logger(config.yml_format.log_path)
