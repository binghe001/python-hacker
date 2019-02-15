#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/15
# Created by 冰河
# Description 检查Skype数据库，把账户信息、联系人地址、通话记录以及存放在数据库中的消息打印出来
#             用法： python meta_skype_sqlite3.py -p <Skype数据库所在的路径>
# 博客 https://blog.csdn.net/l1028386804

import sqlite3
import optparse
import os

#打印用户名、昵称、位置和创建时间
def printProfile(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT fullname, skypename, city, country, datetime(profile_timestamp, 'unixepoch') FROM Accounts;")
    for row in c:
        print '[*] -- Found Account --'
        print '[+] User: ' + str(row(0))
        print '[+] Skype Username: ' + str(row[1])
        print '[+] Location: ' + str(row[2]) + ',' + str(row[3])
        print '[+] Profile Date: ' + str(row[4])

#打印联系人
def printContacts(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;")
    for row in c:
        print '\n[*] --Found Contact --'
        print '[+] User: ' + str(row[0])
        print '[+] Skype Username: ' + str(row[1])
        if str(row[2]) != '' and str(row[2]) != 'None':
            print '[+] Location: ' + str(row[2]) + ',' + str(row[3])
        if str(row[4]) != 'None':
            print '[+] Mobile Number: ' + str(row[4])
        if str(row[5]) != 'None':
            print '[+] Birthday: ' + str(row[5])

#打印通话记录
def printCallLog(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT datetime(begin_timestamp, 'unixepoch'), identity FROM calls, conversations WHERE calls.conv_dbid = conversation.id;")
    print '\n[*] --Found Calls --'
    for row in c:
        print '[+] Time: ' + str(row[0]) + ' | Partner: ' + str(row[1])

#打印消息记录
def printMessage(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT datetime(timestamp, 'unixepoch'), dialog_partner, author, body_xml, FROM Message;")
    print '\n[*] -- Found Message --'
    for row in c:
        try:
            if 'partlist' not in str(row[3]):
                if str(row[1]) != str(row[2]):
                    msgDirection = 'To ' + str(row[1]) + ': '
                else:
                    msgDirection = 'From ' + str(row[2]) + ': '
                print 'Time: ' + str(row[0]) + ' ' + msgDirection + str(row[3])
        except:
            pass

#主函数
def main():
    parser = optparse.OptionParser("usage%prog -p <skype profile path>")
    parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')
    (options, args) = parser.parse_args()
    pathName = options.pathName
    if pathName == None:
        print parser.usage
        exit(0)
    elif os.path.isdir(pathName) == False:
        print '[!] Path Does Not Exist: ' + pathName
        exit(0)
    else:
        skypeDB = os.path.join(pathName, 'main.db')
        if os.path.isfile(skypeDB):
            printProfile(skypeDB)
            printContacts(skypeDB)
            printCallLog(skypeDB)
            printMessage(skypeDB)
        else:
            print '[!] Skype Database does not exist: ' + skypeDB

#程序入口
if __name__ == '__main__':
    main()



