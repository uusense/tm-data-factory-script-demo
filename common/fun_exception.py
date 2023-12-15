# -*- coding: utf-8 -*- 
# @Time : 2022/9/28 22:44 
# @Author : junjie
# @File : fun_exception.py


from functools import wraps
from common.fun_response import CaseResponse
from common.fun_log import mylog
from datetime import datetime

def except_script_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            import traceback
            err_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: " \
                      f"脚本执行异常 -> 执行{func.__name__}函数异常，args：{[*args]}， kwargs：{kwargs}，" \
                      f"报错信息：\n{str(traceback.format_exc())}"
            mylog.error(err_msg)
            return CaseResponse.failed(msg=str(e)), err_msg
    return wrapper