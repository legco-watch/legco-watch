# Local dev settings for scrapy

# Local config for testing
import os

# use this for running scrapy directly
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
FILES_STORE = os.path.join(PROJECT_ROOT, 'datafiles')

# HTTP Caching
# We really do not want to overload the legco server, and it's far faster in development
# to cache results. This turns on file based cache of all HTTP Requests
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = os.path.join(PROJECT_ROOT, 'httpcache')
