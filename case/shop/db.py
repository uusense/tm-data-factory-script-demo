# -*- coding: utf-8 -*- 
# @Time : 2022/8/14 23:05 
# @Author : uusense
# @File : db.py
from common.fun_response import CaseResponse
from common.fun_exception import except_script_error
from datetime import datetime
import pymysql
from loguru import logger


@except_script_error
def sync_db(fromDbConfig, toDbConfig, tables):
    """
    @api {post} /sync_db 数据库表迁移
    @apiGroup 数据库
    @apiName sync_db
    @apiDescription  请求参数，实际只接收from、to、tables，执行时间库表迁移
    @apiPermission uusense
    @apiParam {Object[]} fromDbConfig 源数据库配置
    @apiParam {String} fromDbConfig.host host信息
    @apiParam {String} fromDbConfig.port 端口
    @apiParam {String} fromDbConfig.user 用户
    @apiParam {String} fromDbConfig.password 密码
    @apiParam {String} fromDbConfig.db 数据库名称
    @apiParam {String} fromDbConfig.charset 编码
    @apiParam {Object[]} toDbConfig 目标数据库配置
    @apiParam {String} toDbConfig.host host信息
    @apiParam {String} toDbConfig.port 端口
    @apiParam {String} toDbConfig.user 用户
    @apiParam {String} toDbConfig.password 密码
    @apiParam {String} toDbConfig.db 数据库名称
    @apiParam {String} toDbConfig.charset 编码
    @apiParam {String} tables  迁移表类型
    @apiParamExample {json} 请求示例:
    {
         "fromDbConfig": {
            "host": "192.168.1.70",
            "port": 3306,
            "password": "uusense3412",
            "user": "root",
            "charset": "utf8",
            "db": "datafactory"
         },
         "toDbConfig": {
            "host": "192.168.1.8",
            "port": 3307,
            "user": "root",
            "password": "uusense3412",
            "charset": "utf8",
            "db": "datafactory"
         },
         "tables": "data_factory_cases"
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
    tableList = tables.split(',')
    db_from = pymysql.connect(host=fromDbConfig['host'],
                               port=fromDbConfig['port'],
                               user=fromDbConfig['user'],
                               passwd=fromDbConfig['password'],
                               db=fromDbConfig['db'],
                               charset=fromDbConfig['charset']
                               )
    cursor_from = db_from.cursor()
    # from_sql = 'select description,title from ' + table
    db_to = pymysql.connect(host=toDbConfig['host'],
                               port=toDbConfig['port'],
                               user=toDbConfig['user'],
                               passwd=toDbConfig['password'],
                               db=toDbConfig['db'],
                               charset=toDbConfig['charset']
                               )
    cursor_to = db_to.cursor()
    sourceTables = []
    desTables = []
    msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:检查数据表结构开始!"
    for table in tableList:
        cursor_from.execute("select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA='%s' and TABLE_NAME='%s';" % (fromDbConfig['db'],table))
        sourceTable_tmp = cursor_from.fetchall()
        cursor_to.execute("select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA='%s' and TABLE_NAME='%s';" % (toDbConfig['db'],table))
        desTable_tmp = cursor_to.fetchall()
        if sourceTable_tmp is ():
            sourceTables.append(table)
        if desTable_tmp is not ():
            desTables.append(desTable_tmp[0][0])
    s=d=0
    err_message = ''
    if sourceTables != []:
        err_message += f"迁移源不存在将要迁移的表：,{fromDbConfig['host']},{fromDbConfig['db']}, {sourceTables}, 请检查\n"
        s=1
    if desTables != []:
        err_message += f"目标库存在将要迁移的表：,{toDbConfig['host']},{toDbConfig['db']}, {desTables}, 请移除\n"
        d=1
    if s == 1 or d == 1:
        return CaseResponse.failed(msg='迁移失败'), err_message
    msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:检查数据表结构完成!"
    # to_sql = "insert into data_factory_cases(description, title) value(%s,%s)"
    # len_from = cursor_from.execute(from_sql)
    msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:开始数据同步!\n"
    for table in tableList:
        cursor_from.execute("show create table %s;" % (table))
        createTableSQL = cursor_from.fetchall()[0][1]
        try:
            cursor_to.execute(createTableSQL)
            msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:创建表:{table}\n"
        except Exception as error:
            return CaseResponse.failed(msg= error)
        cursor_from.execute("DESCRIBE %s;" % (table))
        fields = cursor_from.fetchall()
        field_array = [field[0] for field in fields]
        field_str = ','.join(field_array)
        from_sql = "select %s from %s;" % (field_str, table)
        len_from = cursor_from.execute(from_sql)
        to_sql = "insert into %s(%s) value(%s)" % (table, field_str, ','.join(['%s' for i in range(len(field_array))]))
        # to_sql = "insert into data_factory_cases(description, title) value(%s,%s)"
        for i in range(int(len_from)):
            cursor_to.executemany(to_sql, cursor_from.fetchmany(50))
            msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {to_sql}\n"

    # for i in range(int(len_from)):
    #     data1 = cursor_from.fetchmany(50)
    #     cursor_to.executemany(to_sql, data1)
    #     msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {from_sql} -> {to_sql}\n"
    msg += f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:完成数据同步!"
    # data2 = cursor_from.fetchall()
    # cursor_to.executemany(to_sql, data2)
    db_to.commit()
    db_from.close()
    db_to.close()
    return CaseResponse.success(data= "ok"), msg