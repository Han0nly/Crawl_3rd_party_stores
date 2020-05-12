# -*- coding: utf-8 -*-
from pymongo import MongoClient
import bson
import re
if __name__ == '__main__':
    collection = MongoClient('mongodb://localhost:27017/')['scrapy']['Third_Party_apps']
    regax = bson.Regex.from_native(re.compile('^Wandoujia_.*'))
    wandoujia_list = collection.find({'ID':regax},{'ID':1,'Version':1,'file_url':1})
    with open("wandoujia_download.sh",'w') as f:
        f.write('#!/bin/bash\n')
        for item in wandoujia_list:
            index = 0
            if isinstance(item['file_urls'],list):
                for url in item['file_urls']:
                    command = 'wget "'+url+'" -O '+ item['ID']+"_"+item['Version'][index]+"\n"
                    f.write(command)
                    f.write('if [ $? != 0 ];then echo "'+command+'" >> wandoujia_failed.log ;fi\n')
                    index=index+1
            elif isinstance(item['file_urls'],str):
                command = 'wget "' + url + '" -O ' + item['ID'] + "_" + item['Version'] + "\n"
                f.write(command)
                f.write('if [ $? != 0 ];then echo "' + command + '" >> wandoujia_failed.log ;fi\n')
            else:
                pass







