"""
Document wrappers for LegCo Agendas
"""
from django.utils.functional import cached_property
import lxml
from lxml import etree
import re


class CouncilAgenda(object):
    """
    Object representing the Council Agenda document.  This class
    parses the document source and makes all of the individual elements easily accessible
    """
    def __init__(self, source, *args, **kwargs):
        self.source = source
        self.tree = None
        self.tabled_papers = None
        self.other_papers = None
        self.questions = None
        self.motions = None
        self.members_motions_on_legislation = None
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
        # There are also some crazy "zero width joiners" in random places
        # in the text
        # &#8205, &#160 (nbsp)

        self.tree = lxml.html.fromstring(self.source)

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
        pass

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


def load():
    from raw import models, processors, utils
    # Gets agendas since Jan 2013
    objs = models.RawCouncilAgenda.objects.order_by('-uid').all()
    full_files = [processors.get_file_path(xx.local_filename) for xx in objs]
    foo = [utils.check_file_type(xx, as_string=True) for xx in full_files]
    bar = zip(objs, foo, full_files)
    doc_e = bar[60]
    doc_c = bar[61]
    docx_e = bar[0]
    docx_c = bar[1]
    source = utils.docx_to_html(docx_e[2])
    agenda = CouncilAgenda(source)
    return agenda


"""

text = root.xpath('//text()')
pattern = r'^[IV]+\.'
res = []
for p in text:
    if re.search(pattern, p):
        res.append(p)
# res now contains the text of the headers, use getparent() to get elements
headers = [xx.getparent() for xx in res]
# to find the location in the document, we can use iter()

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
