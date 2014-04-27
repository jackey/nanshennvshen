from scrapy.spider import Spider
from scrapy.selector import Selector
from nanshennvshen.items import NanshennvshenItem
from nanshennvshen.library.func import get_desc_from_baike
from nanshennvshen.library.func import get_image_from_baidutu
import urllib
import sys

class BaidupaihangbangSpider (Spider):
	name = "baidupaihangbang"

	urls = [{"url": "http://top.baidu.com/buzz?b=18", "gender": 1},
		{"url": "http://top.baidu.com/buzz?b=16&c=9", "gender": 1},
		{"url": "http://top.baidu.com/buzz?b=3&c=9", "gender": 1},
		{"url": "http://top.baidu.com/buzz?b=17&c=9", "gender": 0},
		{"url": "http://top.baidu.com/buzz?b=15&c=9", "gender": 0},
		{"url": "http://top.baidu.com/buzz?b=22&c=9", "gender": 0}]

	start_urls = []

	def __init__(self, *args, **kwargs):
		super(BaidupaihangbangSpider, self).__init__(*args, **kwargs)
		for url in self.urls:
			self.start_urls.append(url["url"])

	def itemGender(self, url):
		for u in self.urls:
			if u["url"] == url:
				return u["gender"]


	def parse(self, response):
		sel = Selector(response)
		gender = self.itemGender(response.url)
		items = []
		listtable = sel.css("table.list-table tr:not(.item-tr)")
		for index, list_item in enumerate(listtable):
			name = "".join(list_item.css("td.keyword a.list-title::text").extract())
			if name is not "":
				baike = "".join(list_item.css("td.tc a::attr(href)")[0].extract())
				
				shen = NanshennvshenItem()
				shen["name"] = name
				shen["desc"] = get_desc_from_baike(baike)
				shen["image_urls"] = get_image_from_baidutu("http://image.baidu.com/i?tn=baiduimagenojs&ie=utf-8&word="+ urllib.quote(name.encode("utf-8")) +"&s=0")
				items.append(shen)
				shen["gender"] = 1

		return items

