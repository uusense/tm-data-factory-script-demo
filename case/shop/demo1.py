# -*- coding: utf-8 -*- 
# @Time : 2022/8/14 23:05 
# @Author : junjie
# @File : demo.py
from faker import Factory
from common.fun_response import CaseResponse
from common.fun_exception import except_script_error
from datetime import datetime

@except_script_error
def minus(a, b, c):
    """
    @api {post} /minus 三数相减
    @apiGroup 演示
    @apiName minus
    @apiDescription  请求参数只是demo，实际只接收a,b,c，执行三数相减，返回计算结果
    @apiPermission uusense
    @apiParam {String=10000,9999} a=9999    数字类型
    @apiParam {String=10,10} b=10   数字类型
    @apiParam {String=20,20} c=20   数字类型
    @apiParamExample {json} 请求示例:
    {
         "a": "9999",
         "b": "10",
         "c": "20"
      }
    @apiSuccess (200) {Number} code=200 服务器码
    @apiSuccess (200) {String} data="4" 造数成功返回相关的数据
    @apiSuccess (200) {String} msg="造数成功" 提示语
    @apiSuccessExample {json} 返回示例:
    {
        "code": 0,
        "msg": "请求成功",
        "data": 12
    }
    """
    sum = int(a) - int(b) - int(c)
    return CaseResponse.success(data= sum)