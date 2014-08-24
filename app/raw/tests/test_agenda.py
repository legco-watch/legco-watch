# Tests for CouncilAgenda object
from django.test import TestCase
import logging
from raw.docs import agenda


# We use fixtures which are raw HTML versions of the agendas to test the parser
# Each test case works with one source.
logging.disable(logging.CRITICAL)


class Agenda20140709TestCase(TestCase):
    def setUp(self):
        with open('raw/tests/fixtures/council_agenda-20140709-e.html', 'rb') as f:
            self.src = f.read().decode('utf-8')
        self.parser = agenda.CouncilAgenda('council_agenda-20140709-e', self.src)

    def test_tabled_papers_count(self):
        # 8 subsidiary legislation and 29 other papers
        self.assertEqual(len(self.parser.tabled_papers), 37)

    def test_tabled_papers_class(self):
        for p in self.parser.tabled_papers[0:8]:
            self.assertTrue(isinstance(p, agenda.TabledLegislation))

        for p in self.parser.tabled_papers[8:37]:
            self.assertTrue(isinstance(p, agenda.OtherTabledPaper))

    def test_spot_check_tabled_papers(self):
        foo = self.parser.tabled_papers[3]
        self.assertEqual(foo.title, u'Timber Stores (Amendment) Regulation 2014')
        self.assertEqual(foo.number, u'106/2014')

        foo = self.parser.tabled_papers[9]
        self.assertEqual(foo.title, u'No. 120 - Sir Robert Black Trust Fund Report of the Trustee on the Administration of the Fund for the year ended 31 March 2014')
        self.assertEqual(foo.presenter, u'Secretary for Home Affairs')

        foo = self.parser.tabled_papers[27]
        self.assertEqual(foo.title, u'Report of the Panel on Food Safety and Environmental Hygiene 2013-2014')
        self.assertEqual(foo.presenter, u'Dr Hon Helena WONG')

    def test_questions_count(self):
        self.assertEqual(len(self.parser.questions), 22)

    def test_spot_check_questions(self):
        foo = self.parser.questions[8]
        self.assertEqual(foo.asker, u'Hon WONG Yuk-man')
        self.assertEqual(foo.replier, u'Secretary for Security')
        self.assertEqual(foo.type, agenda.AgendaQuestion.QTYPE_WRITTEN)

    def test_bills_count(self):
        pass
