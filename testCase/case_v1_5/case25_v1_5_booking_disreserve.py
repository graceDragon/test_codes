# coding:utf-8
"""
v1.5-集中分散首页-预定列表接口
"""
import unittest
import paramunittest
from common import common
from common.Log import MyLog
import readConfig
from common import configHttp_new
from common import encryptLib
from common import configDB
import json
from config.settings import token_fiel_path


localReadConfig = readConfig.ReadConfig()
# 读取excel表格里的case
tag = int(localReadConfig.get_setting('tag').encode('utf-8'))
guanjia_accounts_xls = common.get_xls("v1.5.xlsx", "booking_disreserve", tag=tag)
print 'excel里测试用例列表:\n', guanjia_accounts_xls


@paramunittest.parametrized(*guanjia_accounts_xls)
class BookingMyDisreserve(unittest.TestCase):
    def setParameters(self, CaseName, CaseDescribe, Method, Token, ServiceID, Data, Result, ExpectState, ExpectMsg):
        """
        初始化excel表格里的数据
        set params
        :param case_name:
        :param method:
        :param token:
        :param data:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(CaseName)
        # CaseDescribe是unicode类型
        self.case_describe = CaseDescribe
        self.method = str(Method)
        self.token = int(Token)
        self.service_id = str(ServiceID)
        self.data = Data
        print 'data数据类型：', type(Data)
        self.result = str(Result)
        self.expect_state = int(ExpectState)
        # unicode转成str类型
        self.expect_msg = ExpectMsg.encode('utf-8')
        self.response = None
        self.info = None

    def description(self):
        """

        :return:
        """
        self.case_describe

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def tearDown(self):
        """

        :return:
        """
        # self.log.build_case_line(self.case_name, str(self.info['err_no']), self.info['err_msg'])

    def test_booking_mydisreserve(self):
        """
        test body
        :return:
        """
        # 给get或者post方法配置Http地址
        self.localConfigHttp = configHttp_new.ConfigHttp(env_old_new='v1.5')
        # 接口地址存储在excel文件里，读取出来
        self.localConfigHttp.set_url(self.service_id)
        # set params
        data = json.loads(self.data)
        # 判断是否需要token
        if self.token == 1:
            f = open(token_fiel_path, 'r')
            token_tmp = f.readline()
            data['access_token'] = token_tmp
            print '获取到的最新token:', data['access_token']
        # 判断是否需要获取验证码
        if 'sms_code' in data:
            sql = localReadConfig.get_sql('sql_yzm')
            yzm = configDB.MyDB().zhiyu_yzm(sql)
            data['sms_code'] = yzm
        # 获取house_id,如果excel表格里house_id为空，则取ini文件里的house_id，否则取excel里的house_id
        if 'house_id' in data:
            if data['house_id'] == '':
                house_id = localReadConfig.get_ini('PARAMS', 'house_id')
                data['house_id'] = house_id
        # # 获取时间戳
        # time_now = common.get_time_now()
        # data['timestamp'] = time_now
        # AES加密
        params_miwen = encryptLib.des_encode_v1_5(data)
        # 真正的入参
        params = {
                'client_id': '586ee968a305374e6198f6b7c293b07a',
                'param': params_miwen
                  }

        self.localConfigHttp.set_params(params)
        # 获取响应结果信息
        if self.method.lower() == 'get':
            self.response = self.localConfigHttp.get()
            print 'get'
        elif self.method.lower() == 'post':
            self.response = self.localConfigHttp.post()
            print 'post'
        # 显示响应结果信息
        common.show_return_msg(self.response)
        self.info = self.response.text
        # Json响应信息转成字典格式
        self.info = json.loads(self.info)
        # 存储token,只有正确登录的时候才有token
        if 'access_token' in self.info['data']:
            token_temp = self.info['data']['access_token']
            localReadConfig.set_headers('token_temp', token_temp)
        # 断言返回状态码
        self.assertEqual(self.info['err_no'], self.expect_state)
        # 断言返回message
        mes_reponse = self.info['err_msg'].encode('utf-8')
        self.assertEqual(mes_reponse, self.expect_msg)


if __name__ == '__main__':
    BookingMyDisreserve().test_booking_mydisreserve()



