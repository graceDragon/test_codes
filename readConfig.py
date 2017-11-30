# coding:utf-8

import os
import codecs
import configparser
import time

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        # fd = open(configPath)
        # data = fd.read()
        #
        # #  remove BOM
        # if data[:3] == codecs.BOM_UTF8:
        #     data = data[3:]
        #     file = codecs.open(configPath, "w")
        #     file.write(data)
        #     file.close()
        # fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        time.sleep(6)
        value = self.cf.get("HEADERS", name)
        print '取最新的token!!!'
        print value
        print time.localtime()
        return value

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_setting(self, name):
        value = self.cf.get("SETTING", name)
        return value

    def get_sql(self, name):
        value = self.cf.get("SQL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_report(self, name):
        value = self.cf.get("Report", name)
        return value

    # def set_headers(self, name, value):
    #     print '存最新的token!!!'
    #     print value
    #     import time
    #     print time.localtime()
    #     with open(configPath, 'w+') as f:
    #         self.cf.set("HEADERS", name, value)
    #         self.cf.write(f)
    #     print '存最新的token!!!完成'
    #     print time.localtime()
    #     print value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        self.cf.write(open(configPath, 'r+'))

        print '存最新的token!!!完成'
        print time.localtime()
        print value

    def set_ini(self, sec, name, value):
        self.cf.add_section(sec)
        self.cf.set(sec, name, value)
        self.cf.write(open(configPath, 'r+'))

    def get_ini(self, sec, name):
        value = self.cf.get(sec, name)
        return value

    def set_report(self, name, value):
        self.cf.set("Report", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)
        # self.cf.write(open(configPath, 'w+'))

    def time_now_second(self):
        # 获取当前时间,到秒
        time_str_s = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        return time_str_s

    def time_now_day(self):
        # 获取当前时间,到天
        time_str_d = time.strftime('%Y%m%d', time.localtime(time.time()))
        return time_str_d


