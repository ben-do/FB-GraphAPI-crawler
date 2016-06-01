# coding=utf-8

import GraphCrawler as GC

if __name__ == '__main__':
    crawler = GC.GraphCrawler(page_name='littlelifer')
    print crawler.get_access_token()
    posts = crawler.get_posts(since="2016-05-28", until="2016-06-01")
    print posts.text
    # print post['data']
