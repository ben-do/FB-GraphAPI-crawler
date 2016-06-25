# coding=utf-8
import json
import os
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
        self.post_data = []

    def get_access_token(self):
        return self.access_token

    def get_posts(self, since=None, until=None):
        # set time range
        since_unix = None
        until_unix = None
        if since is not None:
            since_unix = time.mktime(datetime.datetime.strptime(since, "%Y-%m-%d").timetuple())
        if until is not None:
            until_unix = time.mktime(datetime.datetime.strptime(until, "%Y-%m-%d").timetuple())

        # first request
        payload = {'access_token': self.access_token,
                   'since': since_unix,
                   'until': until_unix
                   }
        r = requests.get(self.base_url + 'posts', params=payload)
        posts = json.loads(r.text)

        for d in posts["data"]:
            self.post_data.append(d)

        # get next page data
        while self.have_paging(posts) is True:
            print "have next page, try to get new post"
            posts = self.load_next(posts)
            for d in posts["data"]:
                self.post_data.append(d)

        return json.loads(r.text)

    def save_posts(self):
        for post in self.post_data:
            file_name = post['id']
            if not os.path.isdir("data/"):
                os.mkdir("data/")

            if "message" in post:
                my_file = open("data/" + file_name, 'w')
                content = post['id'].encode('utf-8') + "\n" + post['created_time'].encode('utf-8') + "\n" + post['message'].encode('utf-8')
                my_file.write(content)
                my_file.close()

    def have_paging(self, posts):
        if "paging" in posts:
            return True
        else:
            return False

    def load_next(self, posts):
        next_url = posts["paging"]["next"]
        next_r = requests.get(next_url)
        # print next_r.text
        next_posts = json.loads(next_r.text)
        return next_posts

    def write_post_into_file(self, file_name="post_data.txt"):
        with open(file_name, 'w') as outfile:
            json.dump(self.post_data, outfile)

    