#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/13
# Created by 冰河
# Description 确定一个FTP服务器是否允许匿名登录，允许则返回True,不允许返回False
# 博客 https://blog.csdn.net/l1028386804

import ftplib

#确认主机是否存在FTP匿名登录
def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print '\n[*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded.'
        ftp.quit()
        return True
    except Exception, e:
        print '\n[-] ' + str(hostname) + ' FTP Anonymous Logon Failed.'
        return False


def main():
    host = raw_input("Please Input Hostname or IP: ")
    while not host:
        host = raw_input("Please Input Hostname or IP: ")
    anonLogin(host)

if __name__ == '__main__':
    main()