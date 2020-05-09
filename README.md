# Crawl_3rd_party_stores

Overview
--------
This is an extensible crawler for downloading Android applications in the third-party markets.
It can crawl the download url addresses of applications and automatically download applications
into repository.



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
* Set the proxy if you have in settings.py
* Set the storage path in settings.py
* Change the mongodb configuration in settings.py
* Start crawler and downloader: 
```
python3 main.py
```


Settings
--------
You can set proxy, user-agen, database name, etc in ```crawler/android_apps_crawler/settings.py``` file.

Supported Third-party Markets
-----------------------------

* Apkpure: https://apkpure.com/ (apkpure.com)
* Baidu: https://shouji.baidu.com/ (shouji.baidu.com)
* Coolapk: https://coolapk.com/ (coolapk.com)
* 360: https://zhushou.360.cn/ (zhushou.360.cn)
* Myapp: https://sj.qq.com/ (sj.qq.com)
* Wandoujia: https://www.wandoujia.com/ (wandoujia.com)
* Xiaomi: http://app.mi.com/ (app.mi.com)
* Keep adding...
