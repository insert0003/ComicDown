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

def main():
    file = open('image.txt')
    imgs = file.readlines()
    file.close()
    
    if not os.path.exists("download"):
        os.makedirs("download")
    
    downDir = os.getcwd()+"/download/"
    print("downDir : ", downDir)

    index = 0
    for url in imgs:
        index = index + 1
        img = urlreq.urlopen(url)
        fname = downDir+str(index).zfill(3)+".jpeg"
        print("save to file: ", fname)
        localfile = open(fname,'wb')
        localfile.write(img.read())
        img.close()
        localfile.close()
    return 

def getImage(pagehref):
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
