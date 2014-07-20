from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import now
import json
import logging
import os
import re
import shutil
import warnings
from raw.models import RawCouncilAgenda, LANG_EN, LANG_CN, RawMember, GENDER_M, GENDER_F
from raw import utils


class BaseProcessor(object):
    """
    Base clase for processing lists of scraped Items and inserting them into the database

    Subclasses should implement a process method
    """
    def __init__(self, items_file_path, job=None):
        self.items_file_path = items_file_path
        self.job = job  # The ScrapeJob, if available
        self._count_created = 0
        self._count_updated = 0


def file_wrapper(fp):
    """
    Yields parsed JSON objects from a line separated JSON file
    """
    if isinstance(fp, basestring):
        with open(fp, 'rb') as fp:
            for line in fp:
                yield json.loads(line)
    else:
        for line in fp:
            yield json.loads(line)


def get_items_file(spider, job_id):
    """
    Return the absolute path for an Items file output by scrapy
    """
    items_folder = getattr(settings, 'SCRAPYD_ITEMS_PATH', None)
    if items_folder is None:
        raise ImproperlyConfigured("No SCRAPY_ITEMS_PATH defined")

    spider_folder = os.path.join(items_folder, 'legcoscraper', spider)
    # extension is either .jl or .json
    file_path = os.path.join(spider_folder, job_id + '.jl')
    if not os.path.exists(file_path):
        file_path = os.path.join(spider_folder, job_id + '.json')
        if not os.path.exists(file_path):
            raise RuntimeError("Could not find items file at {}".format(file_path))
    return file_path

