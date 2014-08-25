#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        self.assertEqual(len(self.parser.bills), 9)

    def test_spot_check_bills(self):
        foo = self.parser.bills[1]
        self.assertEqual(foo.reading, agenda.BillReading.FIRST)
        self.assertEqual(foo.title, u'Land (Miscellaneous Provisions) (Amendment) Bill 2014')
        self.assertEqual(foo.attendees, [])
        
        foo = self.parser.bills[3]
        self.assertEqual(foo.reading, agenda.BillReading.SECOND)
        self.assertEqual(foo.title, u'Land (Miscellaneous Provisions) (Amendment) Bill 2014')
        self.assertEqual(foo.attendees, [u'Secretary for Development'])

        foo = self.parser.bills[7]
        self.assertEqual(foo.reading, agenda.BillReading.SECOND_THIRD)
        self.assertEqual(foo.title, u'Stamp Duty (Amendment) Bill 2013')
        self.assertEqual(len(foo.attendees), 2, foo.attendees)
        self.assertEqual(set(foo.attendees), {u'Secretary for Financial Services and the Treasury',
                                              u'Under Secretary for Financial Services and the Treasury'})
        self.assertEqual(len(foo.amendments), 3)


class Agenda20130508TestCase(TestCase):
    def setUp(self):
        with open('raw/tests/fixtures/council_agenda-20130508-e.html', 'rb') as f:
            self.src = f.read().decode('utf-8')
        self.parser = agenda.CouncilAgenda('council_agenda-20130508-e', self.src)

    def test_count_tabled_papers(self):
        self.assertEqual(len(self.parser.tabled_papers), 9)

    def test_tabled_papers_type(self):
        for p in self.parser.tabled_papers[0:8]:
            self.assertTrue(isinstance(p, agenda.TabledLegislation))

        self.assertTrue(isinstance(self.parser.tabled_papers[8], agenda.OtherTabledPaper))

    def test_spot_check_tabled_papers(self):
        pass

    def test_questions_count(self):
        pass

    def test_spot_check_questions(self):
        pass

    def test_bills_count(self):
        pass

    def test_spot_check_bills(self):
        pass

    def test_motions_count(self):
        pass

    def test_spot_check_motions(self):
        pass


class Agenda20140430TestCase(TestCase):
    def setUp(self):
        with open('raw/tests/fixtures/council_agenda-20140430-c.html', 'rb') as f:
            self.src = f.read().decode('utf-8')
        self.parser = agenda.CouncilAgenda('council_agenda-20130430-c', self.src)

    def test_count_tabled_papers(self):
        self.assertEqual(len(self.parser.tabled_papers), 7)

    def test_tabled_papers_type(self):
        for p in self.parser.tabled_papers[0:4]:
            self.assertTrue(isinstance(p, agenda.TabledLegislation))

        for p in self.parser.tabled_papers[4:7]:
            self.assertTrue(isinstance(p, agenda.OtherTabledPaper))

    def test_spot_check_papers(self):
        pass

    def test_questions_count(self):
        self.assertEqual(len(self.parser.questions), 18)

    def test_questions_spot_check(self):
        foo = self.parser.questions[7]
        self.assertEqual(foo.asker, u'張超雄')
        self.assertEqual(foo.replier, u'發展局局長')
        self.assertEqual(foo.type, agenda.AgendaQuestion.QTYPE_ORAL)

    def test_bills_count(self):
        self.assertEqual(len(self.parser.bills), 9)

    def test_bills_spot_check(self):
        foo = self.parser.bills[2]
        self.assertEqual(foo.title, u'《電子健康紀錄互通系統條例草案》')
        self.assertEqual(foo.attendees, [])
        self.assertEqual(foo.reading, agenda.BillReading.FIRST)

        foo = self.parser.bills[8]
        self.assertEqual(foo.title, u'《2014年撥款條例草案》')
        self.assertEqual(set(foo.attendees), {u'財政司司長'})
        self.assertEqual(foo.reading, agenda.BillReading.THIRD)
