#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/13
# Created by 冰河
# Description 在FTP上搜索网页
# 博客 https://blog.csdn.net/l1028386804

import ftplib

#遍历FTP服务器下的文件，将网页放到数组中并返回数组
def returnDefault(ftp):
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        print '[-] Could not list directory contents.'
        print '[-] Skipping To Next Target.'
        return

    retList = []
    for fileName in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn or '.jsp' in fn:
            print '[+] Found default page: ' + fileName
            retList.append(fileName)

    return retList

#主函数
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

    ftp = ftplib.FTP(host)
    try:
        ftp.login(username, password)
    except Exception, e:
        print e

    retList = returnDefault(ftp)
    if not retList:
        print '\n[-] There is no web page in FTP server.'
        return

    print '\n[+] Find web page:\n'
    for web_page in retList:
        print web_page


if __name__ == '__main__':
    main()