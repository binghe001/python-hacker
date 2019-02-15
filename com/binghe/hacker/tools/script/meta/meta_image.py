#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/15
# Created by 冰河
# Description 下载链接中的所有图片，并检查每张图片中的GPS元数据，若存在GPS元数据，在打印此文件存在GPS元数据
# 博客 https://blog.csdn.net/l1028386804

import urllib2
import optparse
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS

#查找一个链接中的所有图片标签，并把图片标签放到一个数组中返回
def findImages(url):
    print '[+] Finding images on ' + url
    urlContent = urllib2.urlopen(url).read()
    soup = BeautifulSoup(urlContent)
    imgTags = soup.findAll('img')
    return imgTags

#下载图片
def downloadImage(imgTag):
    try:
        print '[+] Downloading image...'
        imgSrc = imgTag['src']
        #将图片的二进制内容读取到变量imgContent中
        imgContent = urllib2.urlopen(imgSrc).read()
        imgFileName = basename(urlsplit(imgSrc)[2])
        imgFile = open(imgFileName, 'wb')
        imgFile.write(imgContent)
        imgFile.close()
        return imgFileName
    except:
        return ''


#检查是否存在GPS，存在则打印出来
def testForExif(imgFileName):
    try:
        exifData = {}
        imgFile = Image.open(imgFileName)
        info = imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifData[decoded] = value
            exifGPS = exifData['GPSInfo']
            if exifData:
                print '[*] ' + imgFileName + ' contains GPS MetaData'
    except:
        pass

#主函数
def main():
    parser = optparse.OptionParser('usage%prog -u <target url>')
    parser.add_option('-u', dest='url', type='string', help='specify url address')
    (options, args) = parser.parse_args()
    url = options.url
    if url == None:
        print parser.usage
        exit(0)
    else:
        imgTags = findImages(url)
        for imgTag in imgTags:
            imgFileName = downloadImage(imgTag)
            testForExif(imgFileName)

if __name__ == '__main__':
    main()

