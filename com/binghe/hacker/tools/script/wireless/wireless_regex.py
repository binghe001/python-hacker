#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 正则表达式验证American Express信用卡
#             更多信息用卡正则信息登录：http://www.regular-expressions.info/credicard.html
# 博客 https://blog.csdn.net/l1028386804

import re

#验证信用卡信息
#确保信用卡卡号是以3开头，第二个字符是4或7，之后是13位数字
def findCredirCard(raw):
    americaRE = re.findall("3[47][0-9]{13}", raw)
    if americaRE:
        print '[+] Found American Express Card: ' + americaRE[0]

def main():
    tests = []
    tests.append('I would like to buy 1337 copies of that dvd')
    tests.append('Bill my card: 378282246310005 for \$2600')
    for test in tests:
        findCredirCard(test)

if __name__ == '__main__':
    main()
