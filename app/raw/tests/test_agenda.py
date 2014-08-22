# Tests for CouncilAgenda object
from django.test import TestCase
import logging
from raw.docs.agenda import CouncilAgenda


# We use fixtures which are raw HTML versions of the agendas to test the parser
# Each test case works with one source.
logging.disable(logging.CRITICAL)


class Agenda20140709TestCase(TestCase):
    def setUp(self):
        with open('raw/tests/fixtures/council_agenda-20140709-e.html', 'rb') as f:
            self.src = f.read().decode('utf-8')
        self.parser = CouncilAgenda('council_agenda-20140709-e', self.src)

    def test_tabled_papers_count(self):
        self.assertEqual(len(self.parser.tabled_papers), 29)
