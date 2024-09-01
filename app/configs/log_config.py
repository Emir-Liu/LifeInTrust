"""
需要在读取配置文件之前的配置的内容，主要是日志，ip获取相关内容
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

# 日志相关配置
# 日志存储路径
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

default_level = logging.INFO

# 对于langchain中自带的log日志信息是否在终端中显示
BOOL_LANGCHAIN_LOG = True


class LoggerOperation:
    """
    对于日志文件的操作类
    """

    def __init__(self):
        self.logger = None

    def get_logger(
        self,
        name,
        log_file: Optional[str] = None,
        level=default_level,
    ):
        """
        返回logger对象
        Returns:

        """

        # 判断logger对象是否已经存在
        if self.logger_exists(name=name):
            self.logger = logging.getLogger(name)

        else:

            self.logger = self.setup_logger(
                name=name,
                log_file=log_file,
                level=level,
            )

        return self.logger

    def logger_exists(self, name):
        """
        判断对应的logger是否存在
        Args:
            name:

        Returns:

        """
        bool_logger_exists = name in logging.Logger.manager.loggerDict

        return bool_logger_exists

    def setup_logger(
        self,
        name: Optional[str] = None,
        log_file: Optional[str] = None,
        level=default_level,
    ):
        """
        建立不同的logger日志信息
        Args:
            name:
            log_file:
            level:

        Returns:

        """
        # 日志存储格式
        logger_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        )

        # 创建logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 创建Handler
        # 控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(fmt=logger_format)

        # 日志文件
        # 如果传入的文件位置为None,则根据name进行拼接
        if log_file == None:
            log_file = os.path.join(LOG_PATH, "{}.log".format(name))

        file_handler = RotatingFileHandler(
            filename=log_file, maxBytes=1024 * 1024 * 10, encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(fmt=logger_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger
