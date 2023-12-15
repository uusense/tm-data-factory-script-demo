# -*- coding: utf-8 -*- 
# @Time : 2022/9/28 23:01 
# @Author : junjie
# @File : fun_log.py

from loguru import logger
from common.FILE_PATH import LOG_FILE_PATH
from datetime import datetime
import os
from functools import wraps


class Logger(object):
    def __init__(self):
        self.logger = logger
        if not os.path.isdir(LOG_FILE_PATH):
            os.mkdir(LOG_FILE_PATH)
        self.logger.add(os.path.join(LOG_FILE_PATH, 'funcase.log'), retention = "5 days")

    def get_logger(self):
        return self.logger

mylog = Logger().get_logger()

class RunLog(object):
    """
    脚本运行日志
    """
    def __init__(self):
        self.log_msg = list()

    def append(self, msg: str, end=False):
        format_str = "[{}]: 脚本结束 -> {}" if end else "[{}]: 脚本开始 -> {}"
        mylog.info(msg)
        self.log_msg.append(format_str.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg))


    def run_add(self, msg: str):
        """
        装饰器日志注入
        :param msg:
        :return:
        """
        self.log_msg.append(msg)

    def o_append(self, msg: str):
        """
        执行脚本日志
        :param msg:
        :return:
        """
        mylog.info("脚本执行 -> {}".format(msg))
        self.log_msg.append("[{}]: 脚本执行 -> {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg))

    def generate(self):
        """
        换行符拼接生成日志
        :return:
        """
        return '\n'.join(self.log_msg)

def case_run_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取函数注释
        func_doc = func.__doc__
        self = args[0]
        mylog.info("脚本开始 -> {}".format(func_doc.strip() if func_doc else func.__name__))
        self.logger.run_add("[{}]: 脚本开始 -> {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                           func_doc.strip() if func_doc else func.__name__))

        result = func(*args, **kwargs)
        mylog.info("脚本结束-> {}".format(func_doc.strip() if func_doc else func.__name__))
        self.logger.run_add("[{}]: 脚本结束 -> {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                  func_doc.strip() if func_doc else func.__name__))

        return result
    return wrapper


if __name__ == '__main__':
    mylog = Logger().get_logger()
    mylog.info("运行成功，返回xxx")