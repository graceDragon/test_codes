# coding:utf-8

import unittest
import paramunittest
from common import common
from common.Log import MyLog
import readConfig
from common import configHttp
from common import encryptLib
import json
from config.settings import token_fiel_path


localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
tag = int(localReadConfig.get_setting('tag').encode('utf-8'))
guanjia_accounts_xls = common.get_xls("guanjia_accounts.xlsx", "test_login", tag=tag)
print '测试用例详细数据列表:\n', guanjia_accounts_xls


@paramunittest.parametrized(*guanjia_accounts_xls)
class GuanJiaLogin(unittest.TestCase):
    def setParameters(self, CaseName, CaseDescribe, Method, Token, ServiceID, Data, Result, ExpectState, ExpectMsg):
        """
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
        self.case_describe = CaseDescribe
        self.method = str(Method)
        self.token = int(Token)
        self.service_id = str(ServiceID)
        data = json.loads(Data)
        self.data = encryptLib.zhiyu_des_encode(data)
        self.result = str(Result)
        self.expect_state = int(ExpectState)
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

    def test_guanjia_login(self):
        """
        test body
        :return:
        """
        # 接口地址存储在excel文件里，然后读取出来
        localConfigHttp.set_url(self.service_id)
        # set params

        params_miwen = self.data

        # 真正的入参
        params = {'client_id': '1fobqa5ofzixluyjlum7icdufabjfo25',
                  'encrypt': 'DES',
                  'param': params_miwen
                  }

        localConfigHttp.set_params(params)
        # # set headers
        # # 添加一个获取token的方法，token可以存储在ini文件里
        # if self.token == '0':
        #     pass
        # elif self.token == '1':
        #     token = localReadConfig.get_headers("token_temp")
        #     headers = {"token": str(token)}
        #     localConfigHttp.set_headers(headers)
        self.response = localConfigHttp.get()
        # check testResult
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        # self.log.build_case_line(self.case_name, str(self.info['err_no']), self.info['err_msg'])

    def checkResult(self):
        # 显示响应信息
        common.show_return_msg(self.response)

        self.info = self.response.text
        # Json响应信息转成字典格式
        self.info = json.loads(self.info)
        # 存储token,只有正确登录的时候才存储token
        if 'access_token' in self.info['data'] and self.info['err_msg'] == 'success':
            token_temp = self.info['data']['access_token']
            # localReadConfig.set_headers('token_temp', token_temp)
            f = open(token_fiel_path, 'w')
            f.write(token_temp)
            print '最新token存储完成...', token_temp

        # 断言返回状态码
        self.assertEqual(self.info['err_no'], self.expect_state)
        # 断言返回message
        mes_reponse = self.info['err_msg'].encode('utf-8')
        self.assertEqual(mes_reponse, self.expect_msg)


if __name__ == '__main__':
    GuanJiaLogin().test_guanjia_login()

