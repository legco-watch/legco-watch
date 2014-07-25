#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Document wrappers for LegCo Agendas
"""
from collections import OrderedDict
import logging
import lxml
from lxml import etree
from lxml.html.clean import clean_html, Cleaner
import re
from lxml.html import HTMLParser
from raw.utils import to_string


logger = logging.getLogger('legcowatch')
QUESTION_PATTERN_E = ur'^\*?([0-9]+)\..*?Hon\s(.*?)\sto ask:'
QUESTION_PATTERN_C = ur'^\*?([0-9]+)\.\s*(.*?)議員問:'


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

    def __init__(self, uid, source, *args, **kwargs):
        self.uid = uid
        if uid[-1] == 'e':
            self.english = True
        else:
            self.english = False
        # Raw html string
        self.source = source
        self.tree = None
        self.tabled_papers = None
        self.questions = None
        self.motions = None
        self.bills = None
        self.members_bills = None
        self.members_motions = None
        self.other = None
        self._headers = []
        self._load()
        self._clean()
        self._parse()

    def __repr__(self):
        return u'<CouncilAgenda: {}>'.format(self.uid)

    def _load(self):
        """
        Load the ElementTree from the source
        """
        # Convert directional quotation marks to regular quotes
        double_quotes = ur'[\u201c\u201d]'
        self.source = re.sub(double_quotes, u'"', self.source)
        single_quotes = ur'[\u2019\u2018]'
        self.source = re.sub(single_quotes, u"'", self.source)
        # Convert colons
        self.source = self.source.replace(u'\uff1a', u':')
        # Remove line breaks and tabs
        self.source = self.source.replace(u'\n', u'')
        self.source = self.source.replace(u'\t', u'')
        # There are also some "zero width joiners" in random places
        # in the text.  Doesn't seem to cause any harm, though, so leave for now
        # these are the codeS: &#8205, &#160 (nbsp), \xa0 (nbsp)

        # Use the lxml cleaner
        cleaner = Cleaner()
        parser = HTMLParser(encoding='utf-8')
        # Finally, load the cleaned string to an ElementTree
        self.tree = cleaner.clean_html(lxml.html.fromstring(to_string(self.source), parser=parser))
        # self.tree = lxml.html.fromstring(to_string(self.source))

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
        # We only want paragraphs and table, since these appear to be the main top level elements
        # ie. we don't want to go fully down the tree
        for elem in self.tree.iter('table', 'p'):
            # When we encounter a header element, figure out what section it is a header for
            text = elem.text_content()
            if text and re.search(pattern, text):
                section_name = self._identify_section(text)
                if section_name is not None:
                    logger.info(u'Identified header {} as {}'.format(text, section_name))
                    current_section = section_name
                else:
                    logger.warn(u"Could not identify section from header {}".format(text))
                    current_section = "other"
                # If this is the first time in this section, initailize the array for storing stuff
                if getattr(self, current_section) is None:
                    setattr(self, current_section, [])
                self._headers.append((current_section, elem))
            else:
                # Add all the elements we encounter to the list for the current section until
                # we encounter another header element, or the end of the document
                if current_section is not None:
                    arr = getattr(self, current_section)
                    arr.append(elem)

        # Once all of the sections are split up, parse each of them separately
        for section in CouncilAgenda.SECTION_MAP.keys():
            if getattr(self, section) is not None:
                getattr(self, "_parse_{}".format(section))()
        # We won't parse others, since we don't know what those are

    def _parse_tabled_papers(self):
        pass

    def _parse_members_bills(self):
        pass

    def _parse_members_motions(self):
        pass

    def _parse_questions(self):
        """
        Parse question lxml elements into AgendaQuestions.

        When this is run, self.questions is a list of lxml elements.  This will
        scan through the list, and give groups of elements that constitute a question
        to the AgendaQuestion constructor.
        """
        if self.questions is not None:
            logger.info(u"Parsing questions from {} elements".format(len(self.questions)))
            parsed_questions = []
            pattern = QUESTION_PATTERN_E if self.english else QUESTION_PATTERN_C
            parts = []
            for q in self.questions:
                content = q.text_content().strip()
                # Discard empty elements
                if content == '':
                    continue
                # Match for question starts
                match = re.match(pattern, content)
                if match is not None:
                    # Found a match for a new question start
                    # If we've accumulated parts for a prior question, clear those out
                    if len(parts) > 0:
                        ag = AgendaQuestion(parts, english=self.english)
                        parsed_questions.append(ag)
                        parts = []
                    logger.debug(u"Found question {}".format(content))
                # Continue to accumulate parts
                parts.append(q)

            # Make sure to parse the last question
            ag = AgendaQuestion(parts, english=self.english)
            parsed_questions.append(ag)
            self.questions = parsed_questions
            logger.info(u"Parsed {} questions".format(len(self.questions)))

    def _parse_bills(self):
        pass

    def _parse_motions(self):
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


class AgendaQuestion(object):
    """
    Object for questions listed in the CouncilAgenda

    Instantiate with the list of lxml elements that comprise
    the question, and this object will parse out the sections
    """
    RESPONDER_PATTERN = ur':\s?(.+)$'

    def __init__(self, elements, english=True):
        self._elements = elements

        # Get the asker
        text = elements[0].text_content()
        pattern = QUESTION_PATTERN_E if english else QUESTION_PATTERN_C
        match = re.match(pattern, text)
        if match is not None:
            self.number = match.group(1)
            self.asker = match.group(2)
        else:
            logger.warn(u'Could not find asker of question in element: {}'.format(text))
            self.asker = None

        # Get the responder
        # If the question is the last question, then there may be a note
        # that begins with an asterisk that says which questions were
        # for written reply
        text = elements[-1].text_content()
        match = re.search(AgendaQuestion.RESPONDER_PATTERN, text)
        if match is not None:
            self.replier = match.group(1)
        else:
            logger.warn(u'Could not find responder of question in element: {}'.format(text))
            self.replier = None

        # Store the rest of the elements into the body as html
        self.body = ''.join([etree.tounicode(xx, method='html') for xx in elements[1:-1]])

    def __repr__(self):
        return u'<Question by {}>'.format(self.asker).encode('utf-8')


class AgendaMotion(object):
    """
    Object for Members' Motions.
    """
    def __init__(self, elements):
        self.mover = None
        self.body = None
        self.amendments = None


class MotionAmendment(object):
    """
    Amendments to motions.
    """
    def __init__(self, parent, elements):
        self.motion = parent
        self.amender = None
        self.body = None


def any_in(arr, iterable):
    """
    Checks if any value in arr is in an iterable
    """
    for elem in arr:
        if elem in iterable:
            return True
    return False


def get_all_agendas():
    from raw import models, utils
    objs = models.RawCouncilAgenda.objects.order_by('-uid').all()
    return objs


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
    res = CouncilAgenda(ag[0].uid, src)
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


from raw.docs.agenda import get_all_agendas, CouncilAgenda
from raw import utils
agendas = get_all_agendas()
objs = []

for ag in agendas:
    objs.append(ag.get_parser())


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


