# -*- coding: utf-8 -*- 
# @Time : 2022/8/14 23:05 
# @Author : alex
# @File : csv2db.py
from common.fun_response import CaseResponse
from common.fun_exception import except_script_error
from datetime import datetime
import pandas as pd
import pymysql
from loguru import logger

@except_script_error
def csv2db(dbConfig, table):
    """
    @api {post} /csv2db 数据库表迁移之cvs导入
    @apiGroup 数据库
    @apiName csv2db
    @apiDescription  请求参数，实际只接收dbConfig、table，执行时间库表迁移
    @apiPermission uusense
    @apiParam {Object[]} dbConfig 数据库配置
    @apiParam {String} dbConfig.host host信息
    @apiParam {String} dbConfig.port 端口
    @apiParam {String} dbConfig.user 用户
    @apiParam {String} dbConfig.password 密码
    @apiParam {String} dbConfig.db 数据库名称
    @apiParam {String} dbConfig.charset 编码
    @apiParam {String} table  迁移表类型
    @apiParamExample {json} 请求示例:
    {
         "dbConfig": {
            "host": "192.168.1.8",
            "port": 3307,
            "password": "uusense3412",
            "user": "root",
            "charset": "utf8",
            "db": "datafactory"
         },
         "table": "cases_operation_log"
      }
    @apiSuccess (200) {Number} code=200 服务器码
    @apiSuccess (200) {String} data="ok" 造数成功返回相关的数据
    @apiSuccess (200) {String} msg="迁移成功" 提示语
    @apiSuccessExample {json} 返回示例:
    {
        "code": 0,
        "msg": "迁移成功",
        "data": "ok"
    }
    """
    db_from = pymysql.connect(host=dbConfig['host'],
                               port=dbConfig['port'],
                               user=dbConfig['user'],
                               passwd=dbConfig['password'],
                               db=dbConfig['db'],
                               charset=dbConfig['charset']
                               )
    cur = db_from.cursor()
    msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:开始同步!\n"
    for chunk in pd.read_csv('git_data/data_factory_script/case/shop/data.csv',sep=',',usecols=['case_id', 'case_type', 'operation_user', 'log_type', 'create_time'],chunksize=1000):
        data = list(zip(chunk['case_id'],chunk['case_type'],chunk['operation_user'],chunk['create_time'],chunk['log_type']))
        query_sql = "insert into "+ table +"(case_id, case_type, operation_user, create_time, log_type) value(%s,%s,%s,%s,%s)"
        try:
            cur.executemany(query_sql,data)
            db_from.commit()
            # msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {data} -> {query_sql}\n"
            print('success')
        except (pymysql.Error,pymysql.Warning) as e:
            db_from.close()
            print(e)
    msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:结束同步!"
    return CaseResponse.success(data= "ok"), msg