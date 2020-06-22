# -*- coding: utf-8 -*-
from pymongo import MongoClient
import bson
import re
if __name__ == '__main__':
    collection = MongoClient('mongodb://localhost:27017/')['scrapy']['Fitness']
    regax = bson.Regex.from_native(re.compile('^Apkpure_.*'))
    wandoujia_list = collection.find({'ID':regax},{'ID':1,'Version':1,'file_urls':1,'file_type':1})
    with open("Apkpure_fitness_download.sh",'w') as f:
        f.write('#!/bin/bash\n')
        for item in wandoujia_list:
            index = 0
            if isinstance(item['file_urls'],list):
                for url in item['file_urls']:
                    try:
                        command = 'wget "'+url+'" -O '+ item['ID']+"_"+item['Version'][index].replace('(','%28').replace(')','%29')+item['file_type'][index]+"\n"
                        error = 'if [ $? -ne 0 ]\nthen\necho wget "'+url+'" -O '+ item['ID']+"_"+item['Version'][index].replace('(','%28').replace(')','%29')+item['file_type'][index]+' >> errors.log\nfi\n'
                    except:
                        command = 'wget "'+url+'" -O '+ item['ID']+"_"+item['Version'][index].replace('(','%28').replace(')','%29')+".apk\n"
                        error = 'if [ $? -ne 0 ]\nthen\necho wget "'+url+'" -O '+ item['ID']+"_"+item['Version'][index].replace('(','%28').replace(')','%29')+'.apk'+' >> errors.log\nfi\n'
                    f.write(command+error+'sleep 2\n')
                    index=index+1
            elif isinstance(item['file_urls'],str):
                try:
                    command = 'wget "' + url + '" -O ' + item['ID'] + "_" + item['Version'].replace('(','%28').replace(')','%29') +item['file_type']+ "\n"
                    error = 'if [ $? -ne 0 ]\nthen\necho wget "'+url+'" -O '+ item['ID']+"_"+item['Version'].replace('(','%28').replace(')','%29')+item['file_type']+' >> errors.log\nfi\n'
                except:
                    command = 'wget "' + url + '" -O ' + item['ID'] + "_" + item['Version'].replace('(','%28').replace(')','%29') + ".apk\n"
                    error = 'if [ $? -ne 0 ]\nthen\necho wget "'+url+'" -O '+ item['ID']+"_"+item['Version'].replace('(','%28').replace(')','%29')+'.apk'+' >> errors.log\nfi\n'
                f.write(command+error+'sleep 2\n')
            else:
                pass








