#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/14
# Created by 冰河
# Description 获取PDF文件中的元数据信息
#             本程序为下载：https://www.wired.com/images_blogs/threatlevel/2010/12/ANONOPS_The_Press_Release.pdf 文件进行分析
#
#             用法： python meta_pdf.py -F pdf文件
# 博客 https://blog.csdn.net/l1028386804

import optparse
from pyPdf import PdfFileReader

#打印元数据信息
def printMeta(fileName):
    pdfFile = PdfFileReader(file(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    print '[*] PDF MetaData For: ' + str(fileName)
    for metaItem in docInfo:
        print '[+] ' + metaItem + ':' + docInfo[metaItem]

def main():
    parser = optparse.OptionParser('usage %prog -F <PDF file name>')
    parser.add_option('-F', dest='fileName', type='string', help='specify PDF file name')
    (options, args) = parser.parse_args()
    fileName = options.fileName
    if fileName == None:
        print parser.usage
        exit(0)
    else:
        printMeta(fileName)

if __name__ == '__main__':
    main()