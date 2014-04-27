

from scrapy.item import Item, Field

class NanshennvshenItem(Item):
    name = Field()
    desc = Field()
    image_urls = Field()
    images = Field()
    gender = Field()

class NanshennvshenDescItem(Item):
	desc = Field()
