# 簡介
建立一個簡單易用的Python小程式來抓取Facebook粉絲專頁上的資訊

# 使用方式
先clone本專案，利用pip 安裝 requests。
```
git clone https://github.com/ben-do/FB-GraphAPI-crawler.git

# (activate your virtual environment)

pip install requests
```
記得將`.env-example`改名為`.env`，並將檔案內的`YOUR_FACEBOOK_ACCESS_TOKEN`替換成你的Access Token

參考程式
```
    # 傳入粉絲專頁的名稱以初始化crawler
    crawler = GC.GraphCrawler(page_name='littlelifer')

    # print crawler.get_access_token()

    # 藉由時間取得粉絲專頁上的po文資料
    crawler.get_posts(since="2016-06-07", until="2016-06-10")

    # 將post資料寫入檔案
    crawler.save_posts()

    # 讀取post的id並取得留言
    crawler.save_all_comments()
```

# QA
* 如何取得facebook的access token?
先 [登記](https://developers.facebook.com/) 成為facebook開發人員
在 [Graph API Explorer](https://developers.facebook.com/tools/explorer/) 中可以看到 Access Token

