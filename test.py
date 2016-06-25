# coding=utf-8

import GraphCrawler as GC
import json

if __name__ == '__main__':
    crawler = GC.GraphCrawler(page_name='littlelifer')
    print crawler.get_access_token()
    posts = crawler.get_posts(since="2016-04-07", until="2016-04-08")
    print crawler.post_data
    # crawler.write_post_into_file()
    # my_file = open("post_data", 'w')
    # my_file.write(str(crawler.post_data))
    # my_file.close()
    # with open('post_data.txt', 'w') as outfile:
    #     json.dump(crawler.post_data, outfile)
    # print posts
    # print posts["data"]
    # for post in posts["data"]:
    #     print post['id']
    # print post['data']
    # for post in posts.text['data']:
    #     print post.data.id

    posts = crawler.save_posts()

