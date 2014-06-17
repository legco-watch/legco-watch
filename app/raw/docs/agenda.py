#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Document wrappers for LegCo Agendas
"""
from collections import OrderedDict
from django.utils.functional import cached_property
import logging
import lxml
from lxml import etree
import re
from raw import models, processors, utils


class CouncilAgenda(object):
    """
    Object representing the Council Agenda document.  This class
    parses the document source and makes all of the individual elements easily accessible
    """
    SECTION_MAP = OrderedDict(
        (
            ('tabled_papers', [u'Tabling of Paper', u'提交文件']),
            ('members_bills', [u"Members' Bill", u"Member's Bill", u'議員法案']),
            ('members_motions', [u"Members' Motion", u"Member's Motion", u'議員議案']),
            ('questions', [u'Question', u'質詢']),
            ('bills', [u'Bill', u'法案']),
            ('motions', [u'Motion', u'議案']),
        )
    )

    def __init__(self, source, *args, **kwargs):
        self.source = source
        self.tree = None
        self.tabled_papers = None
        self.questions = None
        self.motions = None
        self.bills = None
        self.members_bills = None
        self.members_motions = None
        self._load()
        self._clean()
        self._parse()

    def __repr__(self):
        return '<CouncilAgenda>'

    def _load(self):
        """
        Load the ElementTree from the source
        """
        # Convert directional quotation marks to regular quotes
        double_quotes = ur'[\u201c\u201d]'
        self.source = re.sub(double_quotes, u'"', self.source)
        single_quotes = ur'[\u2019\u2018]'
        self.source = re.sub(single_quotes, u"'", self.source)
        # There are also some "zero width joiners" in random places
        # in the text.  Doesn't seem to cause any harm, though, so leave for now
        # these are the codeS: &#8205, &#160 (nbsp), \xa0 (nbsp)

        # Finally, load the cleaned string to an ElementTree
        try:
            self.tree = lxml.html.fromstring(self.source)
        except ValueError:
            # This can throw an error if the source declares an encoding,
            # so give lxml the encoded string
            self.tree = lxml.html.fromstring(self.source.encode('utf-8'))

    def _clean(self):
        """
        Removes some of extraneous tags to make parsing easier
        """
        etree.strip_tags(self.tree, 'strong')
        for xx in self.tree.find_class('pydocx-tab'):
            xx.drop_tag()

    def _parse(self):
        """
        Parse the source document and populate this object's properties
        """
        pattern = ur'^[IV]+\.'
        current_section = None
        # Iterate over the elements in self.tree.iter()
        for elem in self.tree.iter():
            # When we encounter a header element, figure out what section it is a header for
            if elem.text and re.search(pattern, elem.text):
                logging.info(u"Found header: {}".format(elem.text))
                section_name = self._identify_section(elem.text)
                if section_name is not None:
                    logging.info(u'Identified header {} as {}'.format(elem.text, section_name))
                else:
                    logging.warn(u"Could not identify section from header {}".format(elem.text))
            else:
                # Add all the elements we encounter to the list for the current section until
                # we encounter another header element, or the end of the document
                if current_section is not None:
                    pass

    def _identify_section(self, header):
        """
        Try to identify what section the header delineates
        Returns None if it can't identify the section, otherwise it returns the property
        """
        # Need to keep order of the map because we need to check for members' bills before
        # we check for bills

        for prop_name, check_strings in CouncilAgenda.SECTION_MAP.items():
            if any_in(check_strings, header):
                return prop_name
        return None

    def get_headers(self):
        """
        Gets the headers from the document
        """
        text = self.tree.xpath('//text()')
        pattern = ur'^[IV]+\.'
        res = []
        for p in text:
            if re.search(pattern, p):
                res.append(p)
        return res


def any_in(arr, iterable):
    """
    Checks if any value in arr is in an iterable
    """
    for elem in arr:
        if elem in iterable:
            return True
    return False


def get_all_agendas():
    objs = models.RawCouncilAgenda.objects.order_by('-uid').all()
    full_files = [processors.get_file_path(xx.local_filename) for xx in objs]
    file_types = [utils.check_file_type(xx, as_string=True) for xx in full_files]
    zipped = zip(objs, file_types, full_files)
    return zipped


def load():
    # Gets agendas since Jan 2013
    bar = get_all_agendas()
    doc_e = bar[60]
    doc_c = bar[61]
    docx_e = bar[0]
    docx_c = bar[1]
    source = utils.docx_to_html(docx_e[2])
    agenda = CouncilAgenda(source)
    return agenda


"""

# Try to figure out all of the strings that we need to account for
import logging
from raw.docs.agenda import get_all_agendas, CouncilAgenda
from raw import utils
agendas = get_all_agendas()
headers = []
for ag in agendas:
    logging.info(ag)
    if ag[1] == "DOCX":
        src = utils.docx_to_html(ag[2])
    elif ag[1] == "DOC":
        src = utils.doc_to_html(ag[2])
    else:
        continue
    res = CouncilAgenda(src)
    headers.append(res.get_headers())
import itertools
import re
pattern = ur'^[IV]+\.\s?'
flat_headers = list(itertools.chain.from_iterable(headers))
flat_headers = [re.sub(pattern, u'', xx) for xx in flat_headers]
unique_headers = set(flat_headers)
unique_headers = sorted(list(unique_headers))
# there are some headers that get the roman numerals, but miss the title, possibly because of some
# wayward tag

Address by the Chief Executive
Addresses
Bill
Bills
Election of President
Member's Bill
Member's Motion
Members' Bills
Members' Motion
Members' Motions
Members' Motions on Subsidiary Legislation and Other Instruments
Motion
Motions
Question under Rule 24(4) of the Rules of Procedure
Questions
Questions for Written Replies
Questions under Rule 24(4) of the Rules of Procedure
Special Motions
Statements
Tabling of Paper
Tabling of Papers
Taking of Legislative Council Oath
The Chief Executive of the Hong Kong Special Administrative Region   presents the Policy Address
The Chief Executive of the Hong Kong Special Administrative Region  presents the Policy Address
The Chief Executive of the Hong Kong Special Administrative Region  presents the Policy Address to the Council
The Chief Executive's Question and Answer Session
 Motions
以書面答覆的質詢
作出立法會誓言
提交文件
根據《議事規則》第24(4)條提出的質詢
法案
發言
聲明
行政長官發言
行政長官答問會
議員就附屬法例及其他文書提出的議案
議員法案
議員議案
議案
質詢
選舉主席
香港特別行政區行政長官向本會發表施政報告
香港特別行政區行政長官發表施政報告


import logging
from raw.docs.agenda import get_all_agendas, CouncilAgenda
from raw import utils
agendas = get_all_agendas()
objs = []
for ag in agendas[0:20]:
    if ag[1] == "DOCX":
        src = utils.docx_to_html(ag[2])
    elif ag[1] == "DOC":
        src = utils.doc_to_html(ag[2])
    obj = CouncilAgenda(src)
    objs.append(obj)


# clean the html
from lxml.html.clean import clean_html
clean_res = clean_html(res)

# Write to local disk to testing
res = utils.doc_to_html(doc_e[2])
with open('doc_e.html', 'wb') as foo:
    foo.write(res.encode('utf-8'))
res = utils.doc_to_html(doc_c[2])
with open('doc_c.html', 'wb') as foo:
    foo.write(res.encode('utf-8'))

res = pydocx.docx2html(docx_e[2])
with open('docx_e.html', 'wb') as foo:
    foo.write(res.encode('utf-8'))
res = pydocx.docx2html(docx_c[2])
with open('docx_c.html', 'wb') as foo:
    foo.write(res.encode('utf-8'))

import shutil
shutil.copyfile(doc_e[2], './doc_e.doc')
shutil.copyfile(doc_c[2], './doc_c.doc')
shutil.copyfile(docx_e[2], './docx_e.docx')
shutil.copyfile(docx_c[2], './docx_c.docx')

"""
