# coding:utf-8

import os
import unittest
from common.Log import MyLog
import readConfig
from common import HTMLTestRunner
from common.configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        print '日志开始执行...'
        log = MyLog.get_log()
        logger = log.get_logger()
        # html存储路径
        resultPath = log.get_report_path()
        on_off = localReadConfig.get_email("on_off")
        print '获取case路径...'
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseListFile_v1_5 = os.path.join(readConfig.proDir, "caselist_v1_5.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        self.caseList = []

    def set_case_list(self):
        """
        set case list
        :return:
        """
        if True:  # 每次都执行caselist.txt里的case,若不执行则改为if False:
            fb = open(self.caseListFile)
            for line in fb.readlines():
                line = line.strip()
                if line != '' and not line.startswith("#"):
                    # self.caseList.append(line.replace("\n", ""))
                    self.caseList.append(line.split('/')[-1])
            fb.close()
        if True:
            fb_v1_5 = open(self.caseListFile_v1_5)
            for line in fb_v1_5.readlines():
                line = line.strip()
                if line != '' and not line.startswith("#"):
                    # self.caseList.append(line.replace("\n", ""))
                    self.caseList.append(line.split('/')[-1])
            fb_v1_5.close()
        print '获取txt文件里的测试模块...:\n', self.caseList

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()
        for case in self.caseList:
            print '分别获取执行的测试用例模块名称：\n', case
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case)
            for suite in discover:
                for test_name in suite:
                    test_suite.addTest(test_name)
        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            print '获取测试套件...'
            suite = self.set_case_suite()
            if suite is not None:
                logger.info("********测试 开始！********")
                fp = open(resultPath, 'w+')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                       title='Test Report',
                                                       description='若要查看详细结果,请下载附件查看！')
                runner.run(suite)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********测试 结束！*********")
            fp.close()
        # send test report by email
        send_email = MyEmail.get_email()
        if on_off == 'on':
            print '开始发送邮件...'
            send_email.send_email()
            print '邮件发送完成...'
        elif on_off == 'off':
            logger.info("不需要发动邮件给任何人！")
        else:
            logger.info("是否发送邮件的状态码书写错误！")


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
