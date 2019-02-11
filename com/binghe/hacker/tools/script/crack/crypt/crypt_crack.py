#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf-8 -*-
# Date: 2019/2/11
# Created by 冰河
# Description 利用字典破解Unix/Linux口令，根据提示语输入需要破解的密码文件和字典文件即可
# 博客 https://blog.csdn.net/l1028386804

import crypt

#对字典文件中的每一行字符串进行加密，并与原始密码进行比对，是否相同，相同则破解出原始密码的明文并打印出来
def testPass(cryptPass, dictFilePath):
    salt = cryptPass[0:2]
    try:
        dictFile = open(dictFilePath, 'r')
    except Exception, e:
        print e
        return

    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptWord = crypt.crypt(word, salt)
        if(cryptWord == cryptPass):
            print "[+] Found Password: " + word + "\n"
            return

    print "[-] Password Not Found.\n"

#读取并解析密码文件，同时调用testPass方法对密码进行对比
def crack(passwordFile, dictFile):
    try:
        passFile = open(passwordFile, 'r')
    except Exception, e:
        print e
        return

    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            cryptPass = line.split(":")[1].strip(' ')
            print "[*] Cracking Password For: " + user
            testPass(cryptPass, dictFile)

#主函数，设置提示语输入密码文件和字典文件的路径
def main():
    passwordFile = raw_input("Please input PassWord File Path: ")
    while not passwordFile:
        passwordFile = raw_input("Please input PassWord File Path: ")

    dictFile = raw_input("Please input Dictionary File Path: ")
    while not dictFile:
        dictFile = raw_input("Please input Dictionary File Path: ")

    print 'Start Crack Crypt Password...\n'
    crack(passwordFile, dictFile)

#程序的口入
if __name__ == "__main__":
    main()