# -*- coding: utf-8 -*-
from pymongo import MongoClient
if __name__ == '__main__':
    collection = MongoClient('mongodb://localhost:27017/')['scrapy']['Third_Party_apps']
    with open('restart.sh','w') as dest:
        dest.write('#!/bin/bash\n')
        with open('error.log', 'r') as f:
            for line in f:
                info = line.strip().split(' ')
                appid = info[0]
                appversion = info[1]
                failed_item = collection.find_one({'ID': appid}, {'Version': 1, 'file_urls': 1, 'file_type': 1})
                if isinstance(failed_item['file_urls'], list):
                    url = failed_item['file_urls'][failed_item['Version'].index(appversion)]
                    try:
                        type = failed_item['file_type'][failed_item['Version'].index(appversion)]
                    except:
                        type = '.apk'
                else:
                    url = failed_item['file_urls']
                    try:
                        type = failed_item['file_type']
                    except:
                        type = '.apk'
                command = 'wget "' + url + '" -O ' + appid + "_" + appversion.replace('(','%28').replace(')', '%29') + type + "\n"
                error = 'if [ $? -ne 0 ]\nthen\necho "' + appid + " " + appversion + '" >> errors.log\nfi\n'
                dest.write(command+error+'sleep 2\n')


