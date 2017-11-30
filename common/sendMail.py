#!/bin/bash
# coding=utf-8
"""
#######################################################
# filename:mail.py
# author:liuyl
# date:2017-11
# function:发送邮件
#######################################################
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from src import logs
from src.globalLib import *
import src.read_html
from email.utils import parseaddr, formataddr


def _format_address(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_mail_for_board(url, to, subject, attach=False, cc=None, bc=None):
    """发送看板邮件"""
    if cc is None:
        cc = []
    if bc is None:
        bc = []
    to_address = to + cc + bc
    context = src.read_html.get_board_html_for_mail(url)
    if context is False:
        logs().error('html内容为空!!!')
        return False
    msg = MIMEMultipart()
    msg_text = MIMEText(context, _subtype='html', _charset='utf-8')
    msg.attach(msg_text)
    if attach is True:
        report_name = os.path.join('report', get_report_date(), '.html')
        attach = MIMEText(context, "base64", "utf-8")
        attach["Content-Type"] = "application/octet-stream"
        attach["Content-Disposition"] = ("attachment;filename=\"{0}\"".format(report_name)) \
            .decode("utf-8").encode("gb18030")
        msg.attach(attach)

    msg['Subject'] = Header(subject, 'utf-8')
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    msg['To'] = Header('', 'utf-8')
    msg['From'] = _format_address(MAIL_USER)
    if _mail_smtp(MAIL_SMTP_ADDR, MAIL_USER, MAIL_USER_PASSWORD, to_address, msg.as_string()):
        print '邮件发送成功!'
    else:
        print '邮件发送失败!!'


def send_mail_for_develop_auto_push(mailers, report_file, title):
    """开发自触发,发送接口测试报告"""
    to = mailers
    if DEBUG:
        bc = []
    else:
        bc = ['liuyubo@gomeholdings.com', 'wangjianwei@gomeholdings.com', 'duxiaowei@gomeholdings.com']
    cc = []
    to_address = to + cc + bc
    report_name = os.path.basename(report_file)
    msg = MIMEMultipart()  # 构造MIMEMultipart对象做为根容器

    with open(report_file, 'rb') as f:  # 定义正文
        mail_body = f.read()
    msg_text = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg.attach(msg_text)

    attach = MIMEText(mail_body, "base64", "utf-8")
    attach["Content-Type"] = "application/octet-stream"
    attach["Content-Disposition"] = ("attachment;filename=\"{0}\"".format(report_name)) \
        .decode("utf-8").encode("gb18030")
    msg.attach(attach)

    msg['Subject'] = Header(title, 'utf-8')
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')  #
    msg['To'] = Header(str(to), 'utf-8')
    msg['From'] = _format_address(MAIL_USER)

    if _mail_smtp(MAIL_SMTP_ADDR, MAIL_USER, MAIL_USER_PASSWORD, to_address, msg.as_string()):
        print '邮件发送成功!发送人为:', str(to)
    else:
        print '邮件发送失败!!'


def _mail_smtp(smtp_addr, user, user_password, to_addr, mail_msg):
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtp_addr)
        smtp.login(user, user_password)
        smtp.sendmail(MAIL_USER, to_addr, mail_msg)
        return True
    except Exception, err:
        logs().error(err)
        return False
