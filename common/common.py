# coding:utf-8

import requests
import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from . import configHttp
from .Log import MyLog as Log
import json
import time

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
# localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()


caseNo = 0


def get_visitor_token():
    """
    create a token for visitor
    :return:
    """
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host+"/v2/User/Token/generate")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token


def set_visitor_token_to_config():
    """
    set token that created for visitor to config
    :return:
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print u"\n请求地址：\n", url
    print type(msg)
    print u"\n请求信息：\n", msg
    msg_dict = json.loads(msg)
    # 返回值变换格式
    print u"\n请求返回值：\n", json.dumps(msg_dict, ensure_ascii=False, sort_keys=True, indent=4)
    # 请求返回值转成字典格式
    # print(u"\n请求返回值："+'\n'+json.loads(msg))
# ****************************** read testCase excel ********************************


def get_xls(xls_name, sheet_name, tag=0):
    """
    get interface data from xls file
    :return:
    """
    # tag==0 跑所有的测试用例
    # tag==1 跑第1个测试用例
    # tag==2 跑第2个测试用例
    # tag==3 ...
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testData", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    if tag == 0:
        print '跑excel表格里所有测试用例！'
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'CaseName':
                cls.append(sheet.row_values(i))
    else:
        print '跑excel表格里第%s条测试用例' % tag
        cls.append(sheet.row_values(tag))
    return cls

# ****************************** read SQL ********************************
database = {}


def read_sql():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testData", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testData', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/v2/' + '/'.join(url_list)
    return url
# ****************************** read interfaceURL excel ********************************


def get_url_from_excel(xls_name, sheet_name):
    """
    get interface data from excel file
    :return:
    """
    cls = []
    # get excel file's path
    xlsPath = os.path.join(proDir, "testData", 'data', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls
# ****************************** 获取当前时间戳 ********************************


def get_time_now():
    time_now = int(time.time())
    return time_now


if __name__ == "__main__":
    print(get_xls("login"))
    set_visitor_token_to_config()
