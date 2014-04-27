#-*- coding: utf-8 -*-

import BeautifulSoup
import urllib2
import lxml
from lxml.cssselect import CSSSelector
from lxml.etree import fromstring
from nanshennvshen.library.mlstripter import MLScripter
from urlparse import urlparse
import re
import cookielib

def meta_redirect(content, host_name=""):
    soup  = BeautifulSoup.BeautifulSoup(content)

    result=soup.find("meta",attrs={"http-equiv":"Refresh"})
    if result:
        wait,text=result["content"].split(";")
        if text.lower().startswith("url="):
            url=text[4:]
            return host_name + url
    return None

def get_content(url):
    cj = cookielib.CookieJar()
    url_parts = urlparse(url)
    host_name = url_parts.scheme + "://" + url_parts.hostname

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"), 
    ("Referer", "http://baidu.com"),
    ("Accept-Language", "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4"),
    ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36")]

    content = opener.open(url).read()

    # follow the chain of redirects
    while meta_redirect(content):
        u = meta_redirect(content, host_name)
        print u
        content = opener.open(u).read()

    return content

def get_desc_from_baike(url):
    content = get_content(url)
    doc = lxml.html.fromstring(content)
    sel = CSSSelector(".card-summary-content")
    desc = ""

    if len(sel(doc)):
        desc = lxml.html.tostring(sel(doc)[0], encoding="utf-8")
        s = MLScripter()
        s.feed(desc)
        desc = s.get_data()
    if desc is "":
        desc = "稍后马上就会抓取"
    return desc

def get_image_from_baidutu(url):
    html = get_content(url)
    doc = lxml.html.fromstring(html)
    sel = CSSSelector("table#r td a")
    img_urls = []
    if len(sel(doc)):
        for element in sel(doc):
            link = element.get("href")
            pattern = re.compile("objurl=([-:\w\/\.]+)")

            matched = pattern.search(link)
            if matched is not None and matched.group(1):
                img_url = pattern.search(link).group(1)
                img_urls.append(img_url)

            # Max images number is 10
            if len(img_urls) == 10:
                break

    return img_urls

    
