"""
Helpers to load the Scrapy JSON output into RawModels
"""
import json


def file_wrapper(fp):
    """
    Yields parsed JSON objects from a line separated JSON file
    """
    for line in fp:
        yield json.loads(line)
