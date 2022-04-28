import sys

from format import Format
from logger import logger

if __name__ == '__main__':
    try:
        Format()
    except Exception as e:
        logger.error('程序存在异常已经结束 {}'.format(e))
        sys.exit(-1)
