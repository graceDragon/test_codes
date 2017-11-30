# coding:utf-8

import requests
import base64
import json
from common import encryptLib
import binascii
import pyDes
import time


class JieKouTest(object):
    def __init__(self):
        self.url = 'https://dev.efang100.cc/home/houseLists'
        self.data = {
            'page': 1,
            'district_id': 1,
            'location': '',
            'search_name': '芒果',
            'county_id': 1,
            'start_rent': 0,
            'end_rent': 1000,
            'direction': '南',
            'room_amount': 5,
            'feature_id	': 2,
            'tenancy_type': 1,
            'city_id': 1,
            'type_id': 0

        }

    def test_jiekou(self):
        # data = {'source': '1', 'version': '1.0.1',
        #         'mobile': '18211078892', 'password': '18211078892', 'sms_code': '123456'}
        data = {"a":"a","b":"b"}
        str1 = encryptLib.zhiyu_des_encode(data)
        print(str1)

    def jiami(passwd):
        k = pyDes.des("12398711", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5).encrypt(passwd)
        r_hex = binascii.hexlify(k)
        return r_hex

    # r = jiami('diyifangdai')
    # print r
    def test_url(self):
        a = 'hello world!'
        s = base64.encodestring(a)
        s1 = base64.b64encode(a)
        s2 = base64.decodestring(s)
        print s, s1, s2

    def dict_json(self):
        from common.common import get_xls
        path_xls = 'D:\\interfaceTest\\testData\\case\\guanjia_accounts.xlsx'
        sheet_name = 'zhiYu'
        data = get_xls(path_xls, sheet_name)
        print data
        # print type(data[0][5])
        data_dict = data[0][5]
        print data_dict
        print type(data_dict)
        data_dict01 = json.loads(data_dict)
        print data_dict01
        print type(data_dict01)

    def test_info(self):
        import xlrd
        path = 'D:\\interfaceTest\\testData\\case\\guanjia_accounts.xlsx'
        sheet_name = 'info'
        data = xlrd.open_workbook(path)
        # print type(data)
        table = data.sheet_by_name(sheet_name)
        # rows = table.nrows
        # for i in range(rows):
        #     print table.row_values(i)
        data_1 = table.row_values(1)
        print data_1
        print data_1[3]
        print type(data_1[3])

        data_1_dict = json.loads(data_1[3])
        print data_1_dict
        print type(data_1_dict)

        mydata = data_1_dict['aihao']
        print mydata
        print type(mydata)

        mydata_str = mydata.encode('utf-8')
        print mydata_str
        print type(mydata_str)

    def str_int(self):
        a = '5.0'
        b = int(a)
        print b

    def read_ini(self):
        import readConfig
        readConfig.ReadConfig().set_headers('token_temp', '12345678')

    def sql_test(self):
        a = ''
        assert a is ''
        print a
        print type(a)

    def test_read_txt(self):
        import readConfig
        import os
        path = readConfig.proDir
        file_path = os.path.join(path, 'caselist.txt')
        f = open(file_path)
        for line in f.readlines():
            line = line.strip()
            if line != '':
                print line,
                print type(line)

    def test_logging(self):
        import logging
        logging.basicConfig(level=logging.INFO)
        logging.info('this is info')
        logging.debug('this is debug')
        logging.warning('this is warning')

    def test_email(self):
        from email import encoders
        from email.header import Header
        from email.utils import parseaddr, formataddr
        from email.mime.text import MIMEText
        import smtplib

        sender = 'liuyuliang@efang100.com'
        receiver = 'yulianguil@163.com'
        subject = '邮件发送测试'
        server_addr = 'smtp.exmail.qq.com'
        user = 'liuyuliang@efang100.com'
        pwd = 'Lyl112358'

        msg = MIMEText('hello, send by python...', 'plain', 'utf-8')
        msg['subject'] = Header(subject, 'utf-8')

        smtp = smtplib.SMTP()
        smtp.connect(server_addr)
        smtp.login(user, pwd)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()

    def test_strip(self):
        import time
        print time.localtime()

    def test_time_now(self):
        time_now = time.time()
        print int(time_now)

    def test_ini(self):
        import configparser
        import os
        con = configparser.ConfigParser()
        from config.settings import BASEPATH
        file = os.path.join(BASEPATH, 'testini.ini')
        con.read(file)
        v1 = con.get('TEST', 'a')
        print v1
        con.set('TEST', 'a',  '2016')
        con.write(open(file, 'w'))
        v2 = con.get('TEST', 'a')
        print v2

if __name__ == '__main__':
    JieKouTest().test_ini()

    # 111111111112222

