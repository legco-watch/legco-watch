#!/usr/bin/python
# -*- coding: utf-8 -*-

# Tests for MemberName object
from django.test import SimpleTestCase
import logging
from raw.names import MemberName


logging.disable(logging.CRITICAL)


class MemberNameTestCase(SimpleTestCase):
    def test_english_or_chinese(self):
        name = MemberName(u'foo')
        self.assertTrue(name.is_english)

        name = MemberName(u'潘兆平')
        self.assertFalse(name.is_english)

        name = MemberName(u'潘兆平, GBS, JP')
        self.assertFalse(name.is_english)

    def test_minimal_english_name(self):
        name = MemberName(u'Jasper Tsang')
        self.assertEqual(name.last_name, u'Tsang')
        self.assertEqual(name.english_name, u'Jasper')
        self.assertEqual(name.full_name, u'Jasper Tsang')
        for f in ['chinese_name', 'title', 'honours']:
            self.assertIsNone(getattr(name, f))

    def test_anglicized_english_name(self):
        name = MemberName(u'Tsang Yok-sing')
        self.assertEqual(name.last_name, u'Tsang')
        self.assertEqual(name.chinese_name, u'Yok-sing')
        self.assertEqual(name.full_name, u'Yok-sing Tsang')
        for f in ['english_name', 'title', 'honours']:
            self.assertIsNone(getattr(name, f))

    def test_full_english_name(self):
        name = MemberName(u'Hon Jasper TSANG Yok-sing, GBS, JP')
        self.assertEqual(name.last_name, u'Tsang')
        self.assertEqual(name.english_name, u'Jasper')
        self.assertEqual(name.chinese_name, u'Yok-sing')
        # By convention, full name in English is english-name last-name
        # or chinese-name last-name, but not both english-name and chinese-name
        self.assertEqual(name.full_name, u'Jasper Tsang')
        self.assertEqual(name.title, u'Hon')
        self.assertEqual(name.honours, [u'GBS', u'JP'])

    def test_equality_of_english_names(self):
        n1 = MemberName(u'Jasper Tsang')
        n2 = MemberName(u'Hon Jasper TSANG Yok-sing, GBS, JP')
        n3 = MemberName(u'Tsang Yok-sing')
        self.assertEqual(n1, n2)
        self.assertEqual(n2, n3)
        self.assertNotEqual(n1, n3)

    def test_honours_or_title_dont_matter(self):
        n1 = MemberName(u'Jasper TSANG Yok-sing, GBS, JP')
        n2 = MemberName(u'Hon Jasper TSANG Yok-sing, JS')
        n3 = MemberName(u'Mr Jasper TSANG Yok-sing')
        self.assertEqual(n1, n2)
        self.assertEqual(n2, n3)
        self.assertEqual(n1, n3)

    def test_reversed_english_name(self):
        name = MemberName(u'Tsang, Jasper')
        self.assertEqual(name.last_name, u'Tsang')
        self.assertEqual(name.english_name, u'Jasper')
        self.assertEqual(name.full_name, u'Jasper Tsang')
        for f in ['chinese_name', 'title', 'honours']:
            self.assertIsNone(getattr(name, f))

    # def test_reversed_english_with_honours(self):
    #     Does this even happen?
        # name = MemberName(u'Tsang, Jasper, GBS, JP')

    def test_minimal_chinese_name(self):
        name = MemberName(u'曾鈺成')
        self.assertEqual(name.last_name, u'曾')
        self.assertEqual(name.chinese_name, u'鈺成')
        self.assertEqual(name.full_name, u'曾鈺成')
        for f in ['english_name', 'title', 'honours']:
            self.assertIsNone(getattr(name, f))

    def test_full_chinese_name(self):
        name = MemberName(u'曾鈺成議員')
        self.assertEqual(name.last_name, u'曾')
        self.assertEqual(name.chinese_name, u'鈺成')
        self.assertEqual(name.full_name, u'曾鈺成')
        self.assertEqual(name.title, u'議員')
        for f in ['english_name', 'honours']:
            self.assertIsNone(getattr(name, f))

    def test_equality_of_chinese_names(self):
        n1 = MemberName(u'曾鈺成')
        n2 = MemberName(u'曾鈺成議員')
        self.assertEqual(n1, n2)
