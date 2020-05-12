# -*- coding: utf-8 -*-
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['scrapy']
collection = db['Twice']
items = collection.find({"Genre":"Medical","Price":"0"},{"Link": 1 })
fitness = collection.find({"Price":"0","Genre":"Health & Fitness"},{"Link": 1 })
with open("download.sh","w") as f:
    f.write("#!/bin/bash\n")
    for item in items:
        link = item["Link"]
        id = link[46:].split("&")[0]
        command = "gplaycli -L -v -y -av -c ./1.conf -d "+id+" -f ./medical\n"
        f.write(command)
        f.write('if [ $? != 0 ];then echo "' + command + '" >> google_failed.log ;fi\n')
    for item in fitness:
        link = item["Link"]
        id = link[46:].split("&")[0]
        command = "gplaycli -L -v -y -av -c ./1.conf -d "+id+" -f ./fitness\n"
        f.write(command)
        f.write('if [ $? != 0 ];then echo "' + command + '" >> google_failed.log ;fi\n')






