#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 从Twitter上获取数据
# 博客 https://blog.csdn.net/l1028386804

import json
import urllib
from mechainze_browser import *

class ReconPerson:
    def __init__(self, first_name, last_name, job='', social_media={}):
        self.first_name = first_name
        self.last_name = last_name
        self.job = job
        self.social_media = social_media

    def __repr__(self):
        return self.first_name + ' ' + self.last_name + ' has job ' + self.job

    def get_social(self, media_name):
        if self.social_media.has_key(media_name):
            return self.social_media[media_name]
        return None

    def query_twitter(self, query):
        query = urllib.quote_plus(query)
        results = []
        browser = AnonBrowser()
        response = browser.open('http://search.twitter.com/search.json?q=' + query)
        json_objects = json.load(response)
        for result in json_objects['results']:
            new_result = {}
            new_result['name'] = result['name']
            new_result['geo'] = result['geo']
            new_result['tweet'] = result['text']
            results.append(new_result)
        return results

if __name__ == '__main__':
    ap = ReconPerson('Boondock', 'Saint')
    print ap.query_twitter('from:binghe since:2019-02-21 include:retweets')


