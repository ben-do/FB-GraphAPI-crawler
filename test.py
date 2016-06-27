# coding=utf-8

import GraphCrawler as GC


if __name__ == '__main__':

    # 傳入粉絲專頁的名稱以初始化crawler
    crawler = GC.GraphCrawler(page_name='littlelifer')

    # print crawler.get_access_token()

    # 藉由時間取得粉絲專頁上的po文資料
    crawler.get_posts(since="2016-06-07", until="2016-06-10")
    # print crawler.post_data


    # crawler.write_post_into_file()

    # 將post資料寫入檔案
    crawler.save_posts()

    # 讀取post的id並取得留言
    crawler.save_all_comments()
