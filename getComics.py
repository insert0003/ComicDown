#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import os

from bs4 import BeautifulSoup

def main():
    file = open('comic.txt')
    urls = file.readlines()
    file.close()

    for url in urls:
        href = "http://www.cartoonmad.com"
        htmlfp = urllib2.urlopen(url)
        html = htmlfp.read().decode("big5", "replace")
        htmlfp.close()

        soup = BeautifulSoup(html, "lxml")
        mhnew = soup.findAll("table", {"width": '688'})
        title = soup.find("title").text[:-14]
        if not os.path.exists(title):
            os.makedirs(title)
        pdir = os.getcwd()
        os.chdir(title)
   
        for obj in mhnew:
            comic_index = obj.findAll("a")
            for index in comic_index:
                if(index == None):
                    continue
                href = "http://www.cartoonmad.com" + index.get("href")
                num = index.text
                getIndex(href, num)
        os.chdir(pdir)

def getIndex(href, num):
    indexpage = urllib2.urlopen(href)
    index = indexpage.read().decode("utf-8", "replace")
    indexpage.close()
   
    pdir = os.getcwd()
    if not os.path.exists(num):
        os.makedirs(num)
    os.chdir(num)
    
    soup = BeautifulSoup(index, "lxml")
    nav = soup.find("select").findAll("option")
    index = 0
    for mh in nav:
        mhhref = mh.get("value")
        if mhhref:
            index = index + 1
            pic = getImage(mhhref)
            img = urllib.urlopen(pic)
            localfile = open(str(index).zfill(2)+".jpg",'wb')
            localfile.write(img.read())
            img.close()
            localfile.close()
    
    os.chdir(pdir)

    return

def getImage(html):
    pagehref = "http://www.cartoonmad.com/comic/" + html
    page = urllib2.urlopen(pagehref)
    body = page.read().decode("utf-8", "replace")
    page.close()
    
    soup = BeautifulSoup(body, "lxml")
    mhpic = soup.find("img", {"oncontextmenu": 'return false'}).get("src")
    print mhpic
    
    return mhpic

if __name__ == "__main__":
    main()


