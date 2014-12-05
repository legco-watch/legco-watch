# Scrapy settings for legcoscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

BOT_NAME = 'legcoscraper'
SPIDER_MODULES = ['raw.scraper.spiders']
NEWSPIDER_MODULE = 'raw.scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'legcoscraper (+http://odhk.github.io/)'

# Added as per 
# https://groups.google.com/forum/print/msg/scrapy-users/kzGHFjXywuY/O6PIhoT3thsJ
ITEM_PIPELINES = [
    'scrapy.contrib.pipeline.files.FilesPipeline',
]

DATA_DIR_BASE = '/legco-data'
FILES_STORE = os.path.join(DATA_DIR_BASE, 'files')

DOWNLOADER_MIDDLEWARES = {
    # 100 is for the ordering of the middleware pipeline, not for timeout
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 101,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': 102,
}

DOWNLOAD_HANDLERS = {
    # Fix for an exception that gets thrown when a crawler is loaded with boto installed but without AWS credentials
    's3': None
}

# Overriding this. If we do not send Connection: keep-alive, the legco-site will not
# respond to our requests. This is despite it calling Conneciton: close in the response
# Not quite sure why scrapy doesn't send this by default though?
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'Connection': 'keep-alive',
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = os.path.join(DATA_DIR_BASE, 'httpcache')
