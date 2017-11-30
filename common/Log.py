# coding:utf-8

import os
import readConfig
import logging
import threading
from config.settings import report_file_path


localReadConfig = readConfig.ReadConfig()


class Log:
    def __init__(self):
        global logPath, htmlPath, resultPath, proDir
        proDir = readConfig.proDir
        timestr = localReadConfig.time_now_day()
        resultPath = os.path.join(proDir, "testResult")
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        logPath0 = os.path.join(resultPath, "log")

        if not os.path.exists(logPath0):
            os.mkdir(logPath0)
        logPath = os.path.join(logPath0, timestr)
        if not os.path.exists(logPath):
            os.mkdir(logPath)

        htmlPath0 = os.path.join(resultPath, "html")
        if not os.path.exists(htmlPath0):
            os.mkdir(htmlPath0)
        htmlPath = os.path.join(htmlPath0, timestr)
        if not os.path.exists(htmlPath):
            os.mkdir(htmlPath)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)  # 设置DEBUG级别

        # defined handler
        log_name = localReadConfig.time_now_second() + '.log'
        # 创建一个handler，用于写入日志文件
        handler = logging.FileHandler(os.path.join(logPath, log_name))
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        # 日志形式
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(handler)
        # self.logger.addHandler(ch)  # 输出到控制台

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(u'测试结果：' + case_name + " - Code:" + code + " - msg:" + msg)

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_name = localReadConfig.time_now_second() + '.html'
        report_path = os.path.join(htmlPath, report_name)
        # 测试报告路径存储在配置文件里，方便发送邮件时读取报告路径
        # localReadConfig.set_report("report_url", report_path)
        f = open(report_file_path, 'w')
        f.write(report_path)
        print '最新report_path存储完成...', report_path
        return report_path

    def get_result_path(self):
        """
        get test testResult path
        :return:
        """
        return logPath

    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except Exception as ex:
            logger.error(str(ex))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():

        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log

if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")

