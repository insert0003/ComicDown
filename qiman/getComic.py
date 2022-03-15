#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import os, sys
import requests
import json
import js2py
import re
import time
import random

from bs4 import BeautifulSoup

if sys.hexversion >= 0x3000000:
	import urllib.request as urlreq
else:
	import urllib2 as urlreq

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
        url = urls.split(" ")[0]
        startCount = int(urls.split(" ")[1])
        endCount = int(urls.split(" ")[2])

        htmlfp = urlreq.urlopen(url)
        html = htmlfp.read().decode("utf-8", "replace")
        htmlfp.close()

        soup = BeautifulSoup(html, "lxml")

        chapterList = soup.findAll("li", {"class": 'chapter-item'})
        title = soup.find("span", {"class": 'comic-name'}).text

        for obj in chapterList:
            comic_index = obj.find("a")
            if(comic_index == None):
                continue
            if ('通知' in comic_index.text):
                continue
            if ('番外' in comic_index.text):
                continue
            if ('新作推荐' in comic_index.text):
                continue
            href = "http://qiman56.com" + comic_index.get("href")
            # if ('尾声' in comic_index.text):
            #     num = int(comic_index.text.split("尾声")[0])
            # elif ('安教' in comic_index.text):
            #     num = int(comic_index.text.split("安教")[0])
            # else:
            numtext = comic_index.text[0:3]
            num = int(numtext)
            print(num)
            chapter.insert(0, (num, href))


        response = requests.post('http://qiman56.com/bookchapter/', data={"id": 13796, "id2": 1})
        if(response.status_code == 200):
            jsonRes = json.loads(response.text)
            for item in jsonRes:
                if ('通知' in item['name']):
                    continue
                if ('番外' in item['name']):
                    continue
                if ('新作推荐' in item['name']):
                    continue
                href = url + item['id'] + '.html'
                numtext = item['name'][0:3]
                num = int(numtext)
                if (num < startCount):
                    break
                print(num)
                chapter.insert(0, (num, href))

        downImage(chapter, startCount, endCount, downDir)
    return 

def downImage(chapter, startCount, endCount, downDir):
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .\
        NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)', ]

    index = 0
    for num,href in chapter:
        if( num >= startCount and num <= endCount ):
            htmlfp = urlreq.urlopen(href)
            html = htmlfp.read().decode("utf-8", "replace")
            htmlfp.close()
            soup = BeautifulSoup(html, 'html.parser')
            scripts = soup.findAll("script", {"type": "text/javascript"})
            for script in scripts:
                if "eval" in script.text:
                    func = script.text.replace('eval', 'function f() { return ') + '}'
                    break
            result = js2py.eval_js(func)()
            images = re.search(r'var newImgs=\[\"(.*)\"\]', result).group(1)
            imgList = images.split('","')
            curDir = downDir+str(num).zfill(3)+'/'
            print("curDir : ", curDir)
            if not os.path.exists(curDir):
                os.makedirs(curDir)
            for imgUrl in imgList:
                index = index + 1

                img = requests.get(url=imgUrl, headers={'User-Agent': random.choice(ua_list)})
                # img = urlreq.urlopen(imgUrl)
                
                fname = curDir+str(index).zfill(3)+".jpeg"
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
