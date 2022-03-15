#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import os, sys
import re, json
import requests
import base64

import time
import random

from bs4 import BeautifulSoup

if sys.hexversion >= 0x3000000:
	import urllib.request as urlreq
else:
	import urllib2 as urlreq

ua_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .\
    NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)', ]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def main():
    file = open('comic.txt')
    comics = file.readlines()
    file.close()
    
    if not os.path.exists("download"):
        os.makedirs("download")
    
    downDir = os.getcwd()+"/download/"
    print("downDir : ", downDir)

    for urls in comics:
        chapter = []
        comic_id = urls.split(" ")[0].split("/")[-1]
        startCount = int(urls.split(" ")[1])
        endCount = int(urls.split(" ")[2])
        
        url = 'https://m.ac.qq.com/comic/chapterList/id/{}'.format(comic_id)

        html = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'})
        html = html.content.decode("utf-8", "replace")

        soup = BeautifulSoup(html, "lxml")
        section = soup.find('section', {'class': 'chapter-list-box list-expanded'})
        normal_list = section.find('ul', {'class': 'chapter-list normal'})
        for item in normal_list.findAll('a'):
            href = "https://m.ac.qq.com" + item.get("href")
            chapter.append(href)

        downImage(chapter, startCount, endCount, downDir)
    return
        
def downImage(chapter, startCount, endCount, downDir):
    index = 0
    chapterIndex = 0
    for href in chapter:
        chapterIndex = chapterIndex + 1
        if( chapterIndex >= startCount and chapterIndex <= endCount ):
            htmlfp = urlreq.urlopen(href)
            html = htmlfp.read().decode("utf-8", "replace")
            htmlfp.close()
            filter_result = re.search(r"data:\ \'(.*)\'", html).group(1)
            if "InBpY3R1cmUi" in filter_result:
                print('InBpY3R1cmUi in filter_result')
                base64data = filter_result.split("InBpY3R1cmUi")[1]
            elif "cGljdHVyZSI6" in filter_result:
                print('cGljdHVyZSI6 in filter_result')
                base64data = filter_result.split("cGljdHVyZSI6")[1]
            elif "aWN0dXJlIjpb" in filter_result:
                print('aWN0dXJlIjpb in filter_result')
                base64data = filter_result.split("aWN0dXJl")[1]
            else:
                print('can not found flag string href:{} in data:{}'.format(href,filter_result))
            
            dStr = str(base64.b64decode(base64data))
            jsonStr = "[" + re.search(r"\[(.*)\]", dStr).group(1) + "]"
            jsonRes = json.loads(jsonStr)
            for res in jsonRes:
                imgUrl = res["url"].replace("\\/", "/")
                print(imgUrl)
                curDir = downDir+str(chapterIndex).zfill(3)+'/'
                print("curDir : ", curDir)
                if not os.path.exists(curDir):
                    os.makedirs(curDir)

                index = index + 1

                img = requests.get(url=imgUrl, headers={'User-Agent': random.choice(ua_list)})
                
                fname = curDir+str(index).zfill(3)+".jpg"
                print("save to file: ", fname)
                localfile = open(fname,'wb')
                localfile.write(img.content)
                img.close()
                localfile.close()
                time.sleep(1)

            if index >= 140:
                index = 0
    return

if __name__ == "__main__":
    main()

