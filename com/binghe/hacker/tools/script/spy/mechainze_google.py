#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 与Google API交互，
# 博客 https://blog.csdn.net/l1028386804

import urllib
from mechainze_browser import *
import optparse
import json

#存储Google返回的结果数据
class Google_Result:
    def __init__(self, title, text, url):
        self.title = title
        self.text = text
        self.url = url

    def __repr__(self):
        return self.title

#使用Google搜索
def google(search_item):
    ab = AnonBrowser()
    search_item = urllib.quote_plus(search_item)
    response = ab.open('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + search_item)
    objects = json.load(response)
    results = []
    for result in objects['responseData']['results']:
        url = result['url']
        title = result['titleNoFormatting']
        text = result['content']
        new_gr = Google_Result(title, text, url)
        results.append(new_gr)
    return results

def main():
    parser = optparse.OptionParser('usage%prog -k <search keyword>')
    parser.add_option('-k', dest='content', type='string', help='specify search content')
    (options, args) = parser.parse_args()
    content = options.content
    if content == None:
        print parser.usage
        exit(0)
    else:
        results = google(content)
        print results

if __name__ == '__main__':
    main()
