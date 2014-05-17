from django.db import models


LANG_CN = 1
LANG_EN = 2
LANG_CHOICES = (
    (LANG_CN, 'Chinese'),
    (LANG_EN, 'English')
)


class RawModel(models.Model):
    """
    Abstract base class for all raw models
    Provides a few default field, like last_crawled and last_parsed
    """
    # The last time that the raw data was fetched from the LegCo site
    last_crawled = models.DateTimeField(null=True, blank=True)
    # the last time this RawModel was parsed by a parser
    last_parsed = models.DateTimeField(null=True, blank=True)
    # A unique identifier for this type of item
    # We try to generate these as early as possible, but don't enforce a uniqueness constraint
    # for flexibility
    uid = models.CharField(max_length=100, default='')
    # Page from which the Item was crawled
    crawled_from = models.URLField()

    class Meta:
        abstract = True


class RawCouncilAgenda(RawModel):
    """
    Storage of Scrapy items relating to LegCo agenda items

    Should be from the Library Site: http://library.legco.gov.hk:1080/search~S10?/tAgenda+for+the+meeting+of+the+Legislative+Council/tagenda+for+the+meeting+of+the+legislative+council/1%2C670%2C670%2CB/browse
    Will need to adjust if from the LegCo site

    Unclear at the moment if we will be downloading the HTML agendas or the docx version agendas
    """
    # Title of the document.  Should be "Agenda of the meeting of the Legislative Council, <date>"
    title = models.CharField(max_length=255, default='')
    # The LegCo paper number.  Should be "OP <number>" for pre-1997 agendas, or "A <sessionumber>" for later agendas
    paper_number = models.CharField(max_length=50, default='')
    language = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)
    # The URL link to the agenda document
    url = models.URLField(default='')
    # The name of the file saved locally on disk in the scrapy download path
    # Don't use FilePathField or FileField, since those are more for user input via forms
    local_filename = models.CharField(max_length=255, default='')


class RawCouncilVoteResult(RawModel):
    """
    Storage of LegCo vote results
    Sources can be http://www.legco.gov.hk/general/english/open-legco/cm-201314.html or
    http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1314.htm
    """
    # Some meetings span two days, which is why the raw date is a string
    raw_date = models.CharField(max_length=50, default='')
    # URL to the XML file
    xml_url = models.URLField(null=True, blank=True)
    # local filename of the saved XML in the scrapy folder
    xml_filename = models.CharField(max_length=255, default='')
    # URL to the PDF file
    pdf_url = models.URLField(null=True, blank=True)
    # local filename of the saved PDF in the scrapy folder
    pdf_filename = models.CharField(max_length=255, default='')


class RawCouncilHansard(RawModel):
    """
    Storage of LegCo hansard documents
    Sources can be Library: http://library.legco.gov.hk:1080/search~S10?/tHong+Kong+Hansard/thong+kong+hansard/1%2C3690%2C3697%2CB/browse
    or http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1314.htm
    """
    title = models.CharField(max_length=255, default='')
    paper_number = models.CharField(max_length=50, default='')
    language = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)
    url = models.URLField(default='')
    local_filename = models.CharField(max_length=255, default='')


class RawCouncilQuestion(RawModel):
    """
    Storage for Members' questions, from http://www.legco.gov.hk/yr13-14/english/counmtg/question/ques1314.htm#toptbl
    """
    raw_date = models.CharField(max_length=50, default='')
    # Q. 5 <br> (Oral), for example
    number_and_type = models.CharField(max_length=255, default='')
    raised_by = models.CharField(max_length=255, default='')
    subject = models.TextField(default='')
    # Link to the agenda anchor with the text of the question
    subject_link = models.URLField(default='')
    reply_link = models.URLField(default='')
    language = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)
