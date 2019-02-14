#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/14
# Created by 冰河
# Description 恢复Windows回收站中的内容
#             打印所有被删入回收站的文件
#             各个Windows版本的回收站目录如下：
#               1.使用FAT文件的Windows 98及之前的Windows系统: C:\Recycled
#               2.包括Windows NT/2000 和 Windows XP在内的支持NTFS的操作系统: C:\Recycler
#               3.在Windows Vista 和 Windows 7 : C:\$Recycle.Bin
#
#             查询用户的SID
#               命令行切换到回收站所在的目录输入命令dir /a
#               结果为一串数字的字符串，类似于：S-1-5-21-220523388-746137067-682003330-1003
#
#             查询用户SID对应的用户名：
#               命令行输入如下命令查询SID对应的用户名：
#                   reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\<SID>"
#               结果为:ProfileImagePath键存放的值的最后一个反斜杠之后的用户名
#
#               比如：运行命令：C:\>reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\S-1-5-21-220523388-746137067-682003330-1003"
#               得出的结果为：
#                   ProfileImagePath    REG_EXPAND_SZ   %SystemDrive%\Documents and Settings\binghe
#
#                   Sid REG_BINARY      0105000000000005150000007CEB240DEB25792C828BA628EB030000
#
#                   Flags       REG_DWORD       0x0
#                   State       REG_DWORD       0x100
#                   CentralProfile      REG_SZ
#                   ProfileLoadTimeLow  REG_DWORD       0x91172608
#                   ProfileLoadTimeHigh REG_DWORD       0x1d4c416
#                   RefCount    REG_DWORD       0x1
#                   RunLogonScriptSync  REG_DWORD       0x0
#                   OptimizedLogonStatus        REG_DWORD       0xb
#
#                   ProfileImagePath键存放的值的最后一个反斜杠之后的用户名binghe即为SID S-1-5-21-220523388-746137067-682003330-1003对应的用户名
#
# 博客 https://blog.csdn.net/l1028386804

import os
import optparse
from _winreg import *

#将SID转换成对应的用户名
def sid2user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList" + '\\' + sid)
        (value, type) = QueryValueEx(key, 'ProfileImagePath')
        user = value.split('\\')[-1]
        return user
    except:
        return sid

#查找回收站的目录位置，并返回
def returnDir():
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None

#查找系统中所有用户对应的回收站中的文件，并打印出来
def findRecycled(recycleDir):
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        files = os.listdir(recycleDir + sid)
        user = sid2user(sid)
        print '\n[*] Listing Files For User: ' + str(user)
        for file in files:
            print '[+] Found File: ' + str(file)

#主函数
def main():
    recycleDir = returnDir()
    findRecycled(recycleDir)

if __name__ == '__main__':
    main()