# coding:utf-8
"""
管家版本更新
"""

import unittest
import paramunittest
from common import common
from common.Log import MyLog
import readConfig
from common import configHttp
from common import encryptLib
from common import configDB
import json

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
tag = int(localReadConfig.get_setting('tag').encode('utf-8'))
guanjia_accounts_xls = common.get_xls("guanjia_accounts.xlsx", "version_update", tag=tag)
print '测试用例列表:\n', guanjia_accounts_xls


@paramunittest.parametrized(*guanjia_accounts_xls)
class GuanJiaVersionUpdate(unittest.TestCase):
    def setParameters(self, CaseName, CaseDescribe, Method, Token, ServiceID, Data, Result, ExpectState, ExpectMsg):
        """
        执行修改密码测试用例之前，要先执行获取验证码测试用例,也需要先获取token
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
        # json格式转成字典格式
        data = json.loads(Data)
        # 判断是否需要token
        if self.token == '1':
            access_token = localReadConfig.get_headers('token_temp')
            data['access_token'] = access_token
        # 判断是否需要获取验证码
        if 'sms_code' in data:
            sql = localReadConfig.get_sql('sql_yzm')
            yzm = configDB.MyDB().zhiyu_yzm(sql)
            data['sms_code'] = yzm
            # data加密
        print '读取的data', data
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

    def test_version_update(self):
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
        if self.method.lower() == 'get':
            self.response = localConfigHttp.get()
        elif self.method.lower() == 'post':
            self.response = localConfigHttp.post()
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

        # 断言返回状态码
        self.assertEqual(self.info['err_no'], self.expect_state)
        # 断言返回message
        mes_reponse = self.info['err_msg'].encode('utf-8')
        self.assertEqual(mes_reponse, self.expect_msg)


if __name__ == '__main__':
    GuanJiaVersionUpdate().test_version_update()

