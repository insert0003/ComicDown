#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import os, sys
import re, json
import js2py
import requests

import time

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui

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
    file = open('iimh.txt')
    comics = file.readlines()
    file.close()
    
    if not os.path.exists("download"):
        os.makedirs("download")
    
    for urls in comics:
        index = 0
        url = urls.split(" ")[0]
        endCount = int(urls.split(" ")[1])

        chromeOptions = webdriver.ChromeOptions()
        prefs = {'savefile.default_directory': downDir}
        chromeOptions.add_experimental_option("prefs",prefs)
        # chromeOptions.add_argument('--headless')
        driver = webdriver.Chrome(executable_path='./driver/chromedriver', options=chromeOptions)
        driver.get(url)
        time.sleep(2)

        while index < endCount:
            index = index + 1
            nextUrl = downloadImage(driver)
            url = nextUrl
    return

def downloadImage(driver):
    pageDownCount = 0
    while pageDownCount < 20:
        pageDownCount = pageDownCount + 1
        print("scroll down {}".format(pageDownCount))
        pyautogui.hotkey('pagedown')
        time.sleep(1)

    print("ctrl + s")
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    
    print("Enter")
    pyautogui.hotkey('enter')
    time.sleep(30)

    print("NextPage")
    nextPage = driver.find_element_by_xpath('//*[@id="action"]/ul/li[3]/a')
    nextPage.click()
    time.sleep(5)

    print("nextpage is: " + driver.current_url)
    return driver.current_url

if __name__ == "__main__":
    downDir = os.getcwd()+"/download/"
    print("downDir : ", downDir)

    main()

