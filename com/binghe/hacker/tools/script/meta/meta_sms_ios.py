#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/15
# Created by 冰河
# Description 提取IOS备份中的所有短信记录
#             ITunes备份数据目录：
#               Windows: C:\Documents and Settings\<USERNAME>\Application Data\AppleComputer\MobileSync\Backup
#               Mac: /Users/<USERNAME>/Library/Application Support/MobileSync/Backup/
#             用法： python meta_sms_ios.py -p <路径>
#                   python meta_sms_ios.py -p C:\Documents and Settings\<USERNAME>\Application Data\AppleComputer\MobileSync\Backup
#                   python meta_sms_ios.py -p /Users/<USERNAME>/Library/Application Support/MobileSync/Backup/
# 博客 https://blog.csdn.net/l1028386804

import os
import sqlite3
import optparse

#判断是否存在消息表
def isMessageTable(iphoneDB):
    try:
        conn = sqlite3.connect(iphoneDB)
        c = conn.cursor()
        c.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table';")
        for row in c:
            if 'message' in str(row):
                return True
    except:
        return False

#打印消息记录
def printMessage(msgDB):
    try:
        conn = sqlite3.connect(msgDB)
        c = conn.cursor()
        c.execute("SELECT datetime(date, 'unixepoch'), address, text FROM message WHERE address > 0;")
        for row in c:
            date = str(row[0])
            addr = str(row[1])
            text = row[2]
            print '\n Date: ' + date + ', Addr: ' + addr + ', Message: ' + text
    except:
        pass

#主函数
def main():
    parser = optparse.OptionParser("usage%prog -p <iphone Backup Directory>")
    parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')
    (options, args) = parser.parse_args()
    pathName = options.pathName
    if pathName == None:
        print parser.usage
        exit(0)
    else:
        dirList = os.listdir(pathName)
        for fileName in dirList:
            iphoneDB = os.path.join(pathName, fileName)
            if isMessageTable(iphoneDB):
                try:
                    print '\n[*] --- Found Messages ---'
                    printMessage(iphoneDB)
                except:
                    pass

if __name__ == '__main__':
    main()