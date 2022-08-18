#!/usr/bin/env python

import requests
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
from datetime import datetime

import re

import logging


logging.basicConfig(handlers=[logging.FileHandler(filename="./nftevening_paste_scraper.log",
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%F %A %T",
                    level=logging.INFO)
from selenium.webdriver.firefox.options import Options

url = "https://nftevening.com/calendar/past/"
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1280,1024")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-useAutomationExtension")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument("--disable-application-cache")
options.add_argument("--incognito")
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--silent")
#   r,
driver = webdriver.Chrome(options=options)
driver.get(url)

time.sleep(2)


def get_mounth_short_name(sm):
    if len(sm) >=1:
        if sm[0] == "January":
            sm[0] = "Jan"
        elif sm[0] == "February":
            sm[0] = "Feb"
        elif sm[0] == "March":
            sm[0] = "Mar"
        elif sm[0] == "April":
            sm[0] = "Apr"
        elif sm[0] == "June":
            sm[0] = "Jun"
        elif sm[0] == "July":
            sm[0] = "Jul"
        elif sm[0] == "August":
            sm[0] = "Aug"
        elif sm[0] == "September":
            sm[0] = "Sep"
        elif sm[0] == "October":
            sm[0] = "Oct"
        elif sm[0] == "November":
            sm[0] = "Nov"
        elif sm[0] == "December":
            sm[0] = "Dec"
        return sm
    else:
        return ['Jan', '1', '2022']

def get_date(data):
    sm = data
    sm = sm.replace(","," ")
    sm = sm.split()
    # logging.info(sm)
    sm = get_mounth_short_name(sm)
    dd = str(sm[0]) +" "+ str(sm[1]) +" "+ str(sm[2])
    datetime_object = datetime.strptime(dd, '%b %d %Y')
    return datetime_object.strftime('%Y-%m-%dT%H:%M:%S.%f%z')



def extract_url(d,text):
    m = [s for s in d if text in s]
    if len(m)>0:
        return str(m[0])
    else:
        return ""

def get_wp(d):
    for i in d:
        if "twitter" not in i and "discord" not in i and "http" in i and ".png" not in i and ".jpg" not in i and ".jpeg" not in i:
            return i
    else:
        return ""




all_pages = []
page = bs(driver.page_source, "html.parser")

pages = page.findAll('div', attrs={'class' : 'wp-pagenavi'})


pages = pages[0].findAll('a')
pgc = 1
for i in pages:
    tmp = i.get('href')
    tmp = tmp.split("/")
    if int(tmp[-2]) > pgc:
        pgc = int(tmp[-2])
# print(pgc)

pages = []
base = "https://nftevening.com/calendar/past/page/"
for i in range(1, pgc+1):
    pages.append(base + str(i) + "/")


# event sayfaları getirme
events = []
for URL in pages:
    try:
        # print(URL)
        logging.info(URL)
        headersparam = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
        html = requests.get(URL, headers=headersparam, timeout= 10).content
        # print(html)
        data = bs(html, 'html.parser')
        # data = data.findAll('div', {'class': 'event-btns two-btns'})
        # print(data)

        for i in data.findAll('div', {'class': 'event-btns two-btns'}):
            # print("#"*80)
            # print(i)
            # print(type(i))
            events.append(i.find('a')['href'])
            # print(i.find('a')['href'])
            logging.info(i.find('a')['href'])
    except Exception as e:
        print("Problem Occured scraping nft list pages")
        print(URL)
        logging.info(URL)
        logging.info("#"*15)
        logging.info(e)
        logging.info("#"*15)

for URL in events:
    try:
        sm = []
        headersparam = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
        html = requests.get(URL, headers=headersparam, timeout= 10).content
        # print(html)
        data = bs(html, 'html.parser')
        # print(data)
        # drops-socials
        social = data.find('div', {'class': 'drops-socials'})
        social = social.findAll('a')

        # print(URL)
        logging.info(URL)

        for s in social:
            t = s.get('href')
            # print(t)
            sm.append(t)
            # logging.info(t)


        date = data.find('div', {'class': 'drop_date'})
        date = date.text
        #print(date.text)
        #logging.info(date.text)
        date = data.find('div', {'class': 'drop_date'})
        date = date.text
        # print(date.text)
        # logging.info(date.text)

        dt = get_date(date)
        pn =  URL
        wp = get_wp(sm)
        dc = extract_url(sm,"discord")
        tw = extract_url(sm,"twitter")

        data = {"projectname":pn,"twitter":tw,"discord":dc,"website":wp,"datetime":dt}
        logging.info(data)

        # print(data)
        time.sleep(1)
        r = requests.post('http://205.206.228.29:15000/', json=data, auth=(conf.UN,conf.PW))
        logging.info(r.status_code)

    except Exception as e:
        print("Problem Occured")
        print(URL)
        logging.info("#"*15)
        logging.info(e)
        logging.info("#"*15)



