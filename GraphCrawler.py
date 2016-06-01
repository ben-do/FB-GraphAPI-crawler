# coding=utf-8
import json
import requests
import time
import datetime


class GraphCrawler:
    def __init__(self, page_name):
        f = open(".env", 'r')
        setting = json.load(f)
        self.access_token = setting['access_token']
        self.page_name = page_name
        self.base_url = "https://graph.facebook.com/v2.6/%s/" % page_name

    def get_access_token(self):
        return self.access_token

    def get_posts(self, since=None, until=None):
        since_unix = None
        until_unix = None
        if since is not None:
            since_unix = time.mktime(datetime.datetime.strptime(since, "%Y-%m-%d").timetuple())
        if until is not None:
            until_unix = time.mktime(datetime.datetime.strptime(until, "%Y-%m-%d").timetuple())

        payload = {'access_token': self.access_token,
                   'since': since_unix,
                   'until': until_unix
                   }
        r = requests.get(self.base_url + 'posts', params=payload)
        return r

