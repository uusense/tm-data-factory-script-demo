# -*- coding: utf-8 -*- 
# @Time : 2022/8/14 23:05 
# @Author : junjie
# @File : demo.py
from faker import Factory
from common.fun_response import CaseResponse
from common.fun_exception import except_script_error
from datetime import datetime

@except_script_error
def getrandomData():
    """
    @api {post} /getrandomData 随机获取用户注册数据
    @apiGroup 演示
    @apiName getrandomData
    @apiDescription  随机获取身份证、手机号和姓名
    @apiPermission uusense
    @apiSuccess (200) {Integer} code 服务器码
    @apiSuccess (200) {Object} data 造数成功返回相关的数据
    @apiSuccess (200) {String} data.name 名字
    @apiSuccess (200) {String} data.idCard 身份证
    @apiSuccess (200) {String} data.mobile 手机号
    @apiSuccess (200) {String} msg 提示语
    @apiSuccessExample {json} 返回示例:
    {
        "code": 0,
        "msg": "请求成功",
        "data": {
            "name": "uusense",
            "idCard": "440782199510212128",
            "mobile": "13119656023"
        }
    }
    """
    fake = Factory().create('zh_CN')
    name = fake.name()
    id = fake.ssn(min_age=18, max_age=60)
    mobile = fake.phone_number()
    random_data = {
        "name":name,
        "idCard":id,
        "mobile":mobile
    }
    return CaseResponse.success(data=random_data)

def D4createOrder(distributorCode: str, productList: list, account: str = 'sysadmin'):
    """
        @api {post} /D4createOrder 创建D4订单
        @apiGroup 演示
        @apiName D4createOrder
        @apiDescription  创建D4订单
        @apiPermission uusense
        @apiParam {String} distributorCode 配送商编码
        @apiParam {String} account 用户账号
        @apiParam {Object[]} productList 产品数组
        @apiParam {String} productList.productNo 产品编码
        @apiParam {String} productList.car 箱数
        @apiParamExample {json} 请求示例:
        {
                "distributorCode": "888666",
                "account": "sysadmin",
                "productList": [
                    {
                        "productNo": "1314520",
                        "car": "1"
                    }
                ]
            }
        @apiSuccess (200) {Integer} responseCode 服务器码
        @apiSuccess (200) {String} responseMsg 提示语
        @apiSuccess (200) {Object} responseData 造数成功返回相关的数据
        @apiSuccessExample {json} 返回示例:
        {
            "responseCode": 0,
            "responseMsg": "请求成功",
            "responseData": {
            }
        }
        """
    res = productList
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    demo_log = f"""
[{now_time}]: 脚本开始 -> 进行一键创建订单数据
[{now_time}]: 脚本执行 -> 获取登录 token
[{now_time}]: 脚本执行 -> token为xxxxxx
[{now_time}]: 脚本执行 -> 获取商品列表
[{now_time}]: 脚本执行 -> 选中商品
[{now_time}]: 脚本执行 -> 点击立即提交
[{now_time}]: 脚本执行 -> 调转订单确认
[{now_time}]: 脚本执行 -> 调用订单提交接口
[{now_time}]: 脚本结束 -> 进行一键创建订单数据
"""
    return CaseResponse.success(data=res), demo_log