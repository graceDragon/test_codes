# coding:utf-8

import os


"""
env 环境配置，
env = 'test'   执行测试环境相关数据
env = 'online' 执行生产环境相关数据
"""
# ENV_old = 'dev'
ENV_old = 'test'
# ENV_old = 'online'

# ENV_new = 'dev'
ENV_new = 'test'
# ENV_new = 'online'


"""
EMAIL 环境配置
"""
# EMAIL = 'test'
EMAIL = 'online'

BASEPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 临时存储token的路径
token_fiel_path = os.path.join(BASEPATH, 'config\\token.txt')

# 临时存储测试报告的路径
report_file_path = os.path.join(BASEPATH, 'config\\test_report_path.txt')

# 临时存储trac_no邦卡跟踪单号的路径
trac_no_path = os.path.join(BASEPATH, 'config\\trac_no.txt')



