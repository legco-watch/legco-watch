"""
Document wrappers for LegCo Agendas
"""
from django.utils.functional import cached_property


class CouncilAgenda(object):
    """
    Object representing the Council Agenda document.  This class
    parses the document source and makes all of the individual elements easily accessible
    """
    def __init__(self, source, *args, **kwargs):
        self.source = source

    def __repr__(self):
        return '<CouncilAgenda: {}'.format(self.source)

    @cached_property
    def tabled_papers(self):
        pass

    @cached_property
    def other_papers(self):
        pass

    @cached_property
    def questions(self):
        pass

    @cached_property
    def motions(self):
        pass

    @cached_property
    def members_motions_on_legislation(self):
        pass

    @cached_property
    def members_bills(self):
        pass

    @cached_property
    def members_motions(self):
        pass

"""
from raw import models, processors, utils
import subprocess
# Gets agendas since Jan 2013
objs = models.RawCouncilAgenda.objects.order_by('-uid').all()
full_files = [processors.get_file_path(xx.local_filename) for xx in objs]
foo = [utils.check_file_type(xx, as_string=True) for xx in full_files]
bar = zip(objs, foo, full_files)
doc_e = bar[60]
doc_c = bar[61]
res = utils.doc_to_html(doc_e[2])
with open('doc_e.html', 'wb') as foo:
    foo.write(res.encode('utf-8'))
res = utils.doc_to_html(doc_c[2])
with open('doc_c.html', 'wb') as foo:
    foo.write(res.encode('utf-8'))

import pydocx
docx_e = bar[0]
docx_c = bar[1]
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
