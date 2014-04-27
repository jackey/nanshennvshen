# Scrapy settings for nanshennvshen project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nanshennvshen'

SPIDER_MODULES = ['nanshennvshen.spiders']
NEWSPIDER_MODULE = 'nanshennvshen.spiders'


ITEM_PIPELINES = {
	"scrapy.contrib.pipeline.images.ImagesPipeline": 1,
	"nanshennvshen.pipelines.NanshennvshenStoreInToDatabasePipeLine": 500,
}

IMAGES_STORE = '/Users/jackeychen/Workspace/nanshennvshen/crawler/nanshennvshen/images'
IMAGES_MIN_HEIGHT = 200
IMAGES_MIN_WIDTH = 200

API_USER_NAME = "admin"
API_USER_PASS = "admin"
API_HOST = "http://fumer.sourceroot.cn/api/shen"
API_BASE_HOST = "http://fumer.sourceroot.cn/api"

DEFAULT_REQUEST_HEADERS = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
}

DOWNLOAD_DELAY = 1.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nanshennvshen (+http://www.yourdomain.com)'
