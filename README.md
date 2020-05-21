# Crawl_3rd_party_stores

Overview
--------
This is an extensible crawler for downloading Android applications in the third-party markets.
It can crawl the download url addresses of applications and automatically download applications
into repository.

这是一个用于在第三方市场下载Android应用程序的可扩展的爬虫，它可以抓取应用程序的元数据以及下载url地址并自动将应用程序下载到存储库中。

**目前该爬虫只针对于医疗分类，如果要修改为其他分类或整站爬取需要自行修改**


Requirements
------------
* Python 3
* Scrapy (Latest version) & scrapy-mongodb
```
sudo python3 -m pip install scrapy
sudo python3 -m pip install scrapy-mongodb
```

* Mongodb
* Works on Linux, Windows, Mac OSX, BSD
* Currently, downloader cannot work on Windows.

Usage
-----
* Choose the 3rd party market you want to crawl in main.py and comment out the rest of the lines.
* 在main.py中保留你要爬取的站点的那一行，把其余几行代码注释掉
* Start crawler and downloader: 
* 运行：

```
python3 main.py
```


Settings
--------

* Set the proxy if you have in settings.py
* Set the storage path in settings.py
* Change the mongodb configuration in settings.py
* 在settings.py中修改代理/mongodb配置/下载路径
* 豌豆荚的https下载链接从国内访问时会被屏蔽，而用国外服务器下载的话则正常，因此如果需要从国内爬取豌豆荚，需要把从item页面抓取到的下载地址中的https修改为http即可正常下载，境外用户则无需修改

```
# 原程序
item["file_urls"].append(
    Selector(text=r.text).xpath('//a[contains(@class,"normal-dl-btn")]/@href').extract_first())
# 修改为
item["file_urls"].append(
    Selector(text=r.text).xpath('//a[contains(@class,"normal-dl-btn")]/@href').extract_first().replace('https://','http://'))
```

Supported Third-party Markets
-----------------------------

* Apkpure: https://apkpure.com/ (apkpure.com)
* Baidu(百度手机助手): https://shouji.baidu.com/ (shouji.baidu.com)
* Coolapk: https://coolapk.com/ (coolapk.com)
* 360(360手机助手): https://zhushou.360.cn/ (zhushou.360.cn)
* Myapp(应用宝): https://sj.qq.com/ (sj.qq.com)
* Wandoujia(豌豆荚): https://www.wandoujia.com/ (wandoujia.com)
* Xiaomi(小米应用商店): http://app.mi.com/ (app.mi.com)
* Keep adding...
