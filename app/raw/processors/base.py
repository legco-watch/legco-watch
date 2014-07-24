import json


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
        self._count_error = 0


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



