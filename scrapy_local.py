# Local dev settings for scrapy
# This is not the same

# Local config for testing
import os

# use this for running scrapy directly
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
FILES_STORE = os.path.join(PROJECT_ROOT, 'datafiles')
