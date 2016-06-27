# coding=utf-8
import codecs
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

        return self.post_data

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
            if "next" in posts["paging"]:
                return True
        else:
            return False

    def load_next(self, posts):
        next_url = posts["paging"]["next"]
        next_r = requests.get(next_url)
        # print next_r.text
        next_data = json.loads(next_r.text)
        return next_data

    # dump post_data(json object) in to file
    def write_post_into_file(self, file_name="post_data.txt"):
        with open(file_name, 'w') as outfile:
            json.dump(self.post_data, outfile)

    # turn json object or list into file
    def write_obj_into_file(self, obj, file_name="object.txt"):
        with codecs.open(file_name, 'w', 'utf-8') as outfile:
            json.dump(obj, outfile, ensure_ascii=False, indent=4)

    # get comments via object_id
    # return: list
    # object_id: post id
    # save: save the comments into file or not
    def get_comments(self, object_id, save=False):
        comment_list = []
        payload = {'access_token': self.access_token}
        r = requests.get("https://graph.facebook.com/v2.6/" + object_id + "/comments", params=payload)
        comments = json.loads(r.text)
        if "data" in comments:
            for d in comments["data"]:
                if "message" in d:
                    comment_list.append(d["message"])

        # get next page data
        while self.have_paging(comments) is True:
            print "have next page, try to get new comment"
            comments = self.load_next(comments)
            if "data" in comments:
                for d in comments["data"]:
                    if "message" in d:
                        comment_list.append(d["message"])

        # print comment_list
        if save is True:
            if not os.path.isdir("data/comments"):
                os.mkdir("data/comments")
            self.write_obj_into_file(comment_list, "data/comments/%s.txt" % object_id)

        return comment_list

    # save all comments, which from folder "data"'s post
    # 讀取data資料夾內的所有post id, 然後存取留言
    def save_all_comments(self):
        for object_id in os.listdir("data"):
            self.get_comments(object_id, save=True)
