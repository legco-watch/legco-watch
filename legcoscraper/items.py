# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
    
class TypedItem(Item):
    """ Quick extension so you can define type_name on an Item and
        it will get spit out in the JSON format. Replace this if
        you find a better way of achieving this.
    """
    type = Field()

    def __init__(self, *args, **kwargs):
        super(TypedItem, self).__init__(*args, **kwargs)
        self['type'] = self.type_name 

#########################################################
#   ___                  _   _                 
#  / _ \ _   _  ___  ___| |_(_) ___  _ __  ___ 
# | | | | | | |/ _ \/ __| __| |/ _ \| '_ \/ __|
# | |_| | |_| |  __/\__ \ |_| | (_) | | | \__ \
#  \__\_\\__,_|\___||___/\__|_|\___/|_| |_|___/
#                                             

class QuestionRecordQuestion(TypedItem):
    type_name = "QuestionRecordQuestion"

    question_no = Field()
    # The member who raised the question
    raised_by = Field()
    # Was the question originally asked in English or translated?
    was_translated = Field()
    # Was a written reply expected?
    written_reply = Field()
    # The opening text of the question, before the specific articles
    question_text = Field()
    # The question articles. This is a list of items in the form
    # [ (article_id, text), (article_id, text), ... ]
    articles = Field()
    # The officers who are to reply to this question
    # Currently just a blob of text
    officer_to_reply = Field()


class QuestionRecordSubsidiaryPapers(TypedItem):
    type_name = "QuestionRecordSubsidiaryPapers"

    item_no = Field()
    title = Field()
    ln_no = Field()

class QuestionRecordOtherPapers(TypedItem):
    type_name = "QuestionRecordOtherPapers"
    item_no = Field()
    title = Field()
    presented_by = Field()


#########################################################
#  _   _                               _ 
# | | | | __ _ _ __  ___  __ _ _ __ __| |
# | |_| |/ _` | '_ \/ __|/ _` | '__/ _` |
# |  _  | (_| | | | \__ \ (_| | | | (_| |
# |_| |_|\__,_|_| |_|___/\__,_|_|  \__,_|
#                                        

class HansardAgenda(TypedItem):
    """ This will need developed, as it is structured in HTML """
    type_name = "HansardAgenda"
    date = Field()

class HansardMinutes(TypedItem):
    """ This contains a PDF file of the mintues """
    type_name = "HansardMinutes"
    date = Field()
    file_urls = Field()
    files = Field()

class HansardRecord(TypedItem):
    """ This will contain a PDF file for the record for the date """
    type_name = "HansardRecord"
    date = Field()
    language = Field() # Text string - 'en' | 'cn'
    file_urls = Field()
    files = Field()

#####
# Library related items
#####


class LibraryResultPage(TypedItem):
    """
    Stores individual results pages, for debugging
    """
    type_name = "LibraryResultPage"
    # Title of the link
    title = Field()
    link = Field()
    # Page the link was found on
    browse_url = Field()
    # The type of document this page should be fore
    document_type = Field()


class LibraryAgenda(TypedItem):
    """
    Library record for Council Meeting agendas
    """
    type_name = "LibraryAgenda"
    title_en = Field()
    title_cn = Field()
    # List of (title, link) pairs
    links = Field()
    file_urls = Field()
    files = Field()
