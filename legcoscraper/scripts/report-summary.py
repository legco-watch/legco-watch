#!/usr/bin/env python
#
# Give a quick summary of data which has been retrieved
#

import argparse
import json
from collections import Counter
from pprint import pprint
import re

parser = argparse.ArgumentParser()
parser.add_argument("json_file", type=str, help="JSON data file from scraper")
args = parser.parse_args()

type_count = Counter()
year_count = Counter()

year_regex = re.compile('(?P<year>\d\d\d\d)')


infile = open(args.json_file, 'r')
for line in infile.readlines():
    try:
        data_obj = json.loads(line)
    except:
        pass
    type_count[data_obj['type']] += 1

    if data_obj['type'] == 'HansardRecord':
        if data_obj.has_key('date'):
            print data_obj['date'].encode('utf-8')
            match = year_regex.search(data_obj['date'])
            year = int(match.groupdict()['year'])
            year_count[year] += 1
        else:
            print "NO DATE"
            pprint(data_obj)

pprint(dict(type_count))
pprint(dict(year_count))

