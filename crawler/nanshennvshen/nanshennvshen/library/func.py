#-*- coding: utf-8 -*-

import BeautifulSoup
import urllib2
import lxml
from lxml.cssselect import CSSSelector
from lxml.etree import fromstring
from lxml import html
from nanshennvshen.library.mlstripter import MLScripter
from urlparse import urlparse
import re,sys
import cookielib
from PIL import Image
import requests 

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
        content = opener.open(u).read()

    return content

def after_very_baidu_cb(response):
    print response.body

def get_very_form_from_baidu(content):
    doc = html.document_fromstring(content)
    form = doc.xpath(u"//form[@action='http://verify.baidu.com/verify']")
    values = {}
    if len(form):
        # 得到表单元素和值
        for input in form[0].inputs:
            if input.name:
                values[input.name] = input.value
        # 得到验证码的图像
        very_code_img = doc.xpath(u"//div[@id='vf']/img")[0]
        img_content = get_content(very_code_img.get("src"))
        baidu_very_code_local_path = "/tmp/baiduverycode"
        with open(baidu_very_code_local_path, "wb") as f:
            f.write(img_content)
        img = Image.open(baidu_very_code_local_path)
        img.show()
        code = raw_input("请输入您看到的验证码:")
        values["verifycode"] = code
        result = requests.post(form[0].get("action"), values)
        print result
        print values
        sys.exit()
        return True
    else:
        return False

def get_desc_from_baike(url):
    content = get_content(url)
    if get_very_form_from_baidu(content):
        print "WE must very before crawl"
    doc = lxml.html.fromstring(content)
    sel = CSSSelector(".card-summary-content")
    desc = ""

    if len(sel(doc)):
        desc = lxml.html.tostring(sel(doc)[0], encoding="utf-8")
        s = MLScripter()
        s.feed(desc)
        desc = s.get_data()
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
            if len(img_urls) == 15:
                break

    return img_urls

    
