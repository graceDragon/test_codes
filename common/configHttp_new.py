# coding:utf-8
"""
老版的configHttp写死了读取的变量
新版的configHttp_new可以随意赋值来读取
"""
import requests
import readConfig as readConfig
from .Log import MyLog as Log
from config.settings import ENV_new, ENV_old, ENV_1_5


localReadConfig = readConfig.ReadConfig()


class ConfigHttp:
    """
    env_old_new：环境默认为新环境
                env_old_new='new'
    """
    def __init__(self, env_old_new='new', ENV_new='test', ENV_1_5='test'):
        global baseurl
        baseurl = ''
        if env_old_new == 'new':
            print '新接口'
            if ENV_new == 'dev':
                baseurl = 'baseurl_dev_new'
                print 'dev环境'
            elif ENV_new == 'test':
                baseurl = 'baseurl_test_new'
                print 'test环境'
            elif ENV_new == 'xsw':
                baseurl = 'baseurl_xsw_new'
                print 'xsw环境'
        elif env_old_new == 'old':
            print '老接口00'
            if ENV_old == 'dev':
                baseurl = 'baseurl_dev_old'
            elif ENV_old == 'test':
                print '老接口'
                baseurl = 'baseurl_test_old'
        elif env_old_new == 'v1.5':
            print 'v1.5接口'
            if ENV_1_5 == 'dev':
                baseurl = 'baseurl_dev_old_v1_5'
                print 'dev环境'
            elif ENV_1_5 == 'test':
                baseurl = 'baseurl_test_old_v1_5'
                print 'test环境'
            elif ENV_1_5 == 'xsw':
                baseurl = 'baseurl_xsw_old_v1_5'
                print 'xsw环境'
            elif ENV_1_5 == 'ccq':
                baseurl = 'baseurl_ccq_old_v1_5'
                print 'ccq环境'
        self.scheme = localReadConfig.get_http('scheme')
        self.baseurl = localReadConfig.get_http(baseurl)
        port = localReadConfig.get_http("port")
        self.timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = self.scheme+'://' + self.baseurl + url
        print '完整接口地址：', self.url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testData/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(self.timeout))
            # response.raise_for_status()
            return response
        except RuntimeError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            # response = requests.post(self.url, data=self.params)
            response = requests.post(self.url, headers=self.headers, data=self.params, timeout=float(self.timeout))
            # response.raise_for_status()
            print "请求url：", response
            return response
        except RuntimeError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data,
                                     files=self.files, timeout=float(self.timeout))
            return response
        except RuntimeError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(self.timeout))
            return response
        except RuntimeError:
            self.logger.error("Time out!")
            return None

if __name__ == "__main__":
    print("ConfigHTTP")
