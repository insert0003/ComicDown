#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import os

import threading
import time

from bs4 import BeautifulSoup

mutex = [threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock()]
comicDir = ""

class DownThread(threading.Thread):
    """comic down thread"""
    def __init__(self, href, num):
        super(DownThread, self).__init__()
        self.mutexID = int(num) % 5
        self.href = href
        self.num = num

    def run(self):
        global comicDir, mutex
        time.sleep(1)
        if mutex[self.mutexID].acquire():
            indexpage = urllib2.urlopen(self.href)
            index = indexpage.read().decode("utf-8", "replace")
            indexpage.close()
            os.chdir(comicDir)
            if not os.path.exists(self.num):
                os.makedirs(self.num)
            os.chdir(self.num)
            curDir = os.getcwd()+"/"
    
            soup = BeautifulSoup(index, "lxml")
            nav = soup.find("select").findAll("option")
            index = 0
            for mh in nav:
                mhhref = mh.get("value")
                if mhhref:
                    index = index + 1
                    pic = getImage(mhhref)
                    img = urllib.urlopen(pic)
                    fname = curDir+str(index).zfill(2)+".jpg"
                    print fname
                    localfile = open(fname,'wb')
                    localfile.write(img.read())
                    img.close()
                    localfile.close()
                    break
            os.chdir(comicDir)
            mutex[self.mutexID].release()

def main():
    global comicDir
    file = open('comic.txt')
    urls = file.readline()
    file.close()

    url = urls.split(" ")[0] 
    count = urls.split(" ")[1]
    htmlfp = urllib2.urlopen(url)
    html = htmlfp.read().decode("big5", "replace")
    htmlfp.close()

    soup = BeautifulSoup(html, "lxml")
    mhnew = soup.findAll("table", {"width": '688'})
    title = soup.find("title").text[:-14]
    if not os.path.exists(title):
        os.makedirs(title)
    os.chdir(title)
    comicDir = os.getcwd()
    print "comicDir: " + comicDir
   
    for obj in mhnew:
        comic_index = obj.findAll("a")
        for index in comic_index:
            if(index == None):
                continue
            href = "http://www.cartoonmad.com" + index.get("href")
            num = index.text.split(" ")[1]
            if( int(num) > int(count) ):
                mythread = DownThread(href, num)
                mythread.start()

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


