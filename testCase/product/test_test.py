# coding:utf-8

import unittest
import paramunittest
from common import common
from common.Log import MyLog
import readConfig
from common import configHttp

productInfo_xls = common.get_xls("productCase.xlsx", "test_login_old")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()


@paramunittest.parametrized(*productInfo_xls)
class ProductInfo(unittest.TestCase):
    def setParameters(self, case_name, method, token, data, result, code, msg):
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
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.data = data  # data需要根据加密规则进行加密
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def testGetProductInfo(self):
        """
        test body
        :return:
        """
        # set uel
        # self.url = common.get_url_from_xml('productInfo')
        # 接口地址需要存储在ini文件里,或者其他地方，然后读取出来
        self.url = '/common/login'
        localConfigHttp.set_url(self.url)
        # set params

        params = self.data

        localConfigHttp.set_params(params)
        # set headers
        # 添加一个获取token的方法，token可以存储在ini文件里
        if self.token == '0':
            pass
        elif self.token == '1':
            token = localReadConfig.get_headers("token_v")
            headers = {"token": str(token)}
            localConfigHttp.set_headers(headers)
        # get http
        self.response = localConfigHttp.get()
        # check testResult
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        self.info = self.response.json()
        common.show_return_msg(self.response)

        self.assertEqual(self.info['code'], self.code)
        self.assertEqual(self.info['msg'], self.msg)


if __name__ == '__main__':
    ProductInfo().testGetProductInfo()

