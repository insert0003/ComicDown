#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import os, sys

import threading
import time

from bs4 import BeautifulSoup

if sys.hexversion >= 0x3000000:
	import urllib.request as urlreq
else:
	import urllib2 as urlreq

mutex = [threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock()]

class DownThread(threading.Thread):
    """comic down thread"""
    def __init__(self, num, href, volumnDir):
        super(DownThread, self).__init__()
        self.mutexID = int(num) % 5
        self.href = href
        self.volumnDir = volumnDir

    def run(self):
        global mutex
        time.sleep(1)
        if mutex[self.mutexID].acquire():
            if not os.path.exists(self.volumnDir):
                os.makedirs(self.volumnDir)
            os.chdir(self.volumnDir)

            print     
            indexpage = urlreq.urlopen(self.href)
            index = indexpage.read().decode("utf-8", "replace")
            indexpage.close()
            soup = BeautifulSoup(index, "lxml")
            nav = soup.find("select").findAll("option")
            index = 0
            for mh in nav:
                mhhref = mh.get("value")
                if mhhref:
                    index = index + 1
                    pic = getImage(mhhref)
                    img = urlreq.urlopen(pic)
                    fname = self.volumnDir+str(index).zfill(2)+".jpg"
                    print("save to file: ", fname)
                    localfile = open(fname,'wb')
                    localfile.write(img.read())
                    img.close()
                    localfile.close()
            mutex[self.mutexID].release()

def main():
    file = open('comic.txt')
    comics = file.readlines()
    file.close()
    
    if not os.path.exists("download"):
        os.makedirs("download")
    
    downDir = os.getcwd()+"/download"
    print("downDir : ", downDir)

    for urls in comics:
        url = urls.split(" ")[0]
        startCount = int(urls.split(" ")[1])
        endCount = int(urls.split(" ")[2])

        htmlfp = urlreq.urlopen(url)
        html = htmlfp.read().decode("big5", "replace")
        htmlfp.close()

        soup = BeautifulSoup(html, "lxml")
        mhnew = soup.findAll("table", {"width": '688'})
        title = soup.find("title").text[:-14]
        if(os.name == "posix"):
            title = title.encode("utf8")

        for obj in mhnew:
            comic_index = obj.findAll("a")
            for index in comic_index:
                if(index == None):
                    continue
                if len(index.text.split(" ")) < 3:
                    continue

                href = "http://www.cartoonmad.com" + index.get("href")
                num = int(index.text.split(" ")[1])
                if( num >= startCount and num <= endCount ):
                    print("Getting {} vol.{} from {}.".format(title, num, href))
                    volumnDir = "{}/{}/{}/".format(downDir, title, num)
                    mythread = DownThread(num, href, volumnDir)
                    mythread.start()
    return 

def getImage(html):
    pagehref = "http://www.cartoonmad.com/comic/" + html
    page = urlreq.urlopen(pagehref)
    body = page.read().decode("utf-8", "replace")
    page.close()
    mhpic = ""
    
    soup = BeautifulSoup(body, "lxml")
    mhsrc = soup.find("img", {"oncontextmenu": 'return false'})
    if mhsrc != None:
        mhpic = mhsrc.get("src")
    print("image source: ", mhpic)
    
    return mhpic

if __name__ == "__main__":
    main()
