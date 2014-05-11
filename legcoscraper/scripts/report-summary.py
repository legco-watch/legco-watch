#!/usr/bin/env python
#
# Give a quick summary of data which has been retrieved
#

import argparse
import json
from collections import Counter
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("json_file", type=str, help="JSON data file from scraper")
args = parser.parse_args()

type_count = Counter()

infile = open(args.json_file, 'r')
for line in infile.readlines():
    try:
        data_obj = json.loads(line)
    except:
        pass
    type_count[data_obj['type']] += 1

pprint(dict(type_count))

