#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/22
# Created by 冰河
# Description 使用smtplib发送电子邮件
#             用法： python smtplib_send_email.py -u <from username> -p <from password> -t <to email address> -s <subject> -c <text> -a <smtp address> -P <smtp port>
#             例如： python smtplib_send_email.py -u 用户名 -p 密码 -t 接收邮件的地址 -s 主题 -c 邮件内容 -a smtp.qq.com -P 25
# 博客 https://blog.csdn.net/l1028386804

import smtplib
import optparse
from email.mime.text import MIMEText

#发送邮件
def sendMail(user, pwd, to, subject, text, smtp_address, smtp_port):
    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject
    try:
        smtpServer = smtplib.SMTP(smtp_address, smtp_port)
        print '[+] Connecting To EMail Server.'
        smtpServer.ehlo()
        print '[+] Starting Encrypted Session.'
        smtpServer.starttls()
        smtpServer.ehlo()
        print '[+] Logging Into Mail Server.'
        smtpServer.login(user, pwd)
        print '[+] Sending Mail.'
        smtpServer.sendmail(user, to, msg.as_string())
        smtpServer.close()
        print '[+] Mail Sent Successfully.'
    except Exception, e:
        print '[+] Sending Mail Failed.'
        print e

def main():
    parser = optparse.OptionParser('usage%prog -u <from username> -p <from password> -t <to email address> -s <subject> -c <text> -a <smtp address> -P <smtp port>')
    parser.add_option('-u', dest='user', type='string', help='specify from username')
    parser.add_option('-p', dest='pwd', type='string', help='specify from password')
    parser.add_option('-t', dest='to', type='string', help='specify to email address')
    parser.add_option('-s', dest='subject', type='string', help='specify subject')
    parser.add_option('-c', dest='text', type='string', help='specify text')
    parser.add_option('-a', dest='smtp_address', type='string', help='specify smtp address')
    parser.add_option('-P', dest='smtp_port', type='int', help='specify smtp port')
    (options, args) = parser.parse_args()
    user = options.user
    pwd = options.pwd
    to = options.to
    subject = options.subject
    text = options.text
    smtp_address = options.smtp_address
    smtp_port = options.smtp_port

    if user == None or pwd == None or to == None or subject == None or text == None or smtp_address == None or smtp_port == None:
        print parser.usage
        exit(0)
    sendMail(user, pwd, to, subject, text, smtp_address, smtp_port)

if __name__ == '__main__':
    main()
