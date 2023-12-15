# -*- coding: utf-8 -*- 
# @Time : 2022/9/28 22:43 
# @Author : junjie
# @File : fun_response.py

class CaseResponse(object):

    @staticmethod
    def success(code=0, msg="执行脚本成功", data=None, **kwargs) -> dict:
        content = dict(responseCode=code, responseMsg=msg, responsedata=data)
        if kwargs and isinstance(data, dict): data.update(kwargs)
        return content

    @staticmethod
    def failed(code=400, msg="执行脚本失败", data=None, **kwargs) -> dict:
        content = dict(responseCode=code, responseMsg=msg, responsedata=data)
        if kwargs and isinstance(data, dict): data.update(kwargs)
        return content