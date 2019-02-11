#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf-8 -*-
# Date: 2019/2/11
# Created by 冰河
# Description 
# 博客 https://blog.csdn.net/l1028386804

import zipfile
from threading import Thread

#执行解压操作
def extractFile(zFile, password):
    try:
        zFile.extractall(pwd = password)
        print '[+] Found Password ' + password + '\n'
    except:
        return

def crackZip(zipFile, dicFile):
    zFile = zipfile.ZipFile(zipFile)
    try:
        passFile = open(dicFile)
    except Exception, e:
        return

    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()

#主函数
def main():
    zipFile = raw_input('Please input the Zip File Path: ')
    while not zipFile:
        zipFile = raw_input('Please input the Zip File Path: ')

    dicFile = raw_input('Please input the Dictionary File Path: ')
    while not dicFile:
        dicFile = raw_input('Please input the Dictionary File Path: ')

    crackZip(zipFile, dicFile)

if __name__ == "__main__":
    main()