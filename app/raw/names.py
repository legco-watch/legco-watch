#!/usr/bin/python
# -*- coding: utf-8 -*-
import re


def is_ascii(string):
    """
    Check for unicode encoded characters by trying to encode the string as ascii only
    """
    try:
        string.encode('ascii')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return False
    else:
        return True


def proper(string):
    """
    Proper cases a string.  Handles None.  Doesn't use builtin str.title() because this capitalizes letters
    after a dash - e.g. "Yok-Sing" whereas we want "Yok-sing"
    :param string: string or None
    :return: string or None
    """
    if isinstance(string, basestring):
        string = string[:1].upper() + string[1:].lower()
    return string


class MemberName(object):
    def __init__(self, full_name=None, english_name=None, last_name=None, chinese_name=None):
        """
        Initialize with either a string that represents the full name, or the components of the full_name
        in keyword arguments
        """
        self.is_english = True
        self.title = None
        self.english_name = None
        self.last_name = None
        self.chinese_name = None
        self.honours = None
        if full_name is None:
            # No full name, so use the components
            if not is_ascii(last_name):
                self.is_english = False
            self.english_name = proper(english_name)
            self.last_name = proper(last_name)
            self.chinese_name = proper(chinese_name)
        else:
            # Check for language, then call the relevant parser
            if is_ascii(full_name):
                self._parse_english_name(full_name)
            else:
                self._parse_chinese_name(full_name)
                self.is_english = False

    def __repr__(self):
        return u'<MemberName: {}>'.format(self.full_name)

    def __eq__(self, other):
        """
        For English names:
        Last names must match.  If both Chinese name and English name are present, then both must match.
        If one or the other is present, then they must match.
        A name with both Chinese and English names can match a name with only one or the other.
        For example Jasper Tsang Yok-sing will match Tsang Yok-sing, but the latter will not match Jasper Tsang.
        """
        # If all nulls, then no matches
        if self.last_name is None or other.last_name is None:
            return False
        if self.english_name is None and self.chinese_name is None:
            return False
        if other.english_name is None and other.chinese_name is None:
            return False

        # If full names match, we can all go home
        # Chinese names are caught here
        if self.full_name == other.full_name:
            return True

        # Otherwise, do more complex checks
        if self.last_name != other.last_name:
            return False

        if self.english_name is not None and other.english_name is not None and self.english_name == other.english_name:
            if self.chinese_name is not None and other.chinese_name is not None and self.chinese_name != other.chinese_name:
                return False
            else:
                return True

        if self.chinese_name is not None and other.chinese_name is not None and self.chinese_name == other.chinese_name:
            if self.english_name is not None and other.english_name is not None and self.english_name != other.english_name:
                return False
            else:
                return True

        return False

    def _parse_english_name(self, name):
        """
        Given an english full name, try to parse it into its constituent parts
        """
        title_re = ur'(?P<title>Mr|Mrs|Miss|Ms|Hon|Dr)'
        ename_re = ur'(?P<fname>[a-zA-Z]+)'
        lname_cap_re = ur'(?P<lname>[A-Z]{2,})'
        lname_re = ur'(?P<lname>[a-zA-Z]+)'
        # We assume that the anglicized Chinese names consist of three characters, though there are definitely
        # some members for whom this is not the case.
        cname_re = ur'(?P<cname>[a-zA-Z]+-{1}[a-zA-Z]+)'
        fully_qualified = ur'^{}? ?{} {} {}?(, )?(?P<hon>[A-Z, ]+)?'.format(title_re, ename_re, lname_cap_re, cname_re)
        match = re.match(fully_qualified, name)
        if match is not None:
            res = match.groupdict()
            self.english_name = proper(res['fname'])
            self.title = proper(res['title'])
            if res['hon'] is not None:
                self.honours = [xx.strip() for xx in res['hon'].split(',') if xx is not None]
            self.last_name = proper(res['lname'])
            self.chinese_name = proper(res['cname'])
            return

        english_with_anglicized = ur'{} {} {}'.format(ename_re, lname_re, cname_re)
        match = re.search(english_with_anglicized, name)
        if match is not None:
            res = match.groupdict()
            self.english_name = proper(res['fname'])
            self.last_name = proper(res['lname'])
            self.chinese_name = proper(res['cname'])
            return

        minimal_with_cap = ur'{} {}'.format(ename_re, lname_cap_re)
        match = re.search(minimal_with_cap, name)
        if match is not None:
            res = match.groupdict()
            self.english_name = proper(res['fname'])
            self.last_name = proper(res['lname'])
            return

        minimal_anglicized = ur'{} {}'.format(lname_re, cname_re)
        match = re.search(minimal_anglicized, name)
        if match is not None:
            res = match.groupdict()
            self.last_name = proper(res['lname'])
            self.chinese_name = proper(res['cname'])
            return

        reversed = ur'{}, {}'.format(lname_re, ename_re)
        match = re.search(reversed, name)
        if match is not None:
            res = match.groupdict()
            self.last_name = proper(res['lname'])
            self.english_name = proper(res['fname'])
            return

        minimal = ur'{} {}'.format(ename_re, lname_re)
        match = re.search(minimal, name)
        if match is not None:
            res = match.groupdict()
            self.last_name = proper(res['lname'])
            self.english_name = proper(res['fname'])
            return

    def _parse_chinese_name(self, name):
        """
        Given a chinese name, parse it into its constituent parts
        """
        # Assumes that Chinese names are 3 characters.
        cname_re = ur'^(?P<name>\w{2,3})(?P<title>議員)?$'
        match = re.match(cname_re, name, re.UNICODE)
        if match is not None:
            res = match.groupdict()
            self.last_name = res['name'][0]
            self.chinese_name = res['name'][1:3]
            self.title = res['title']
            return

    @property
    def full_name(self):
        if self.is_english:
            if self.english_name is not None:
                if self.chinese_name is not None:
                    return u'{} {} {}'.format(self.english_name, self.last_name, self.chinese_name)
                else:
                    return u'{} {}'.format(self.english_name, self.last_name)
            else:
                return u'{} {}'.format(self.chinese_name, self.last_name)
        else:
            return u'{}{}'.format(self.last_name, self.chinese_name)


class NameMatcher(object):
    """
    Searcher class which takes a collection of MemberNames and stores them in a last name based index
    Chinese names are stored by the Chinese character, so the index can grow quite large
    """
    def __init__(self, names):
        """
        :param names: list of MemberNames or list of tuples where MemberName is the first element in each tuple
        """
        self._index = {}
        for n in names:
            if isinstance(n, MemberName):
                first_letter = n.last_name[0].lower()
            else:
                first_letter = n[0].last_name[0].lower()
            if self._index.get(first_letter, None) is None:
                self._index[first_letter] = []
            self._index[first_letter].append(n)

    def match(self, name):
        """
        Given an instance of MemberName, find a name in the index that matches it

        :param name: MemberName
        :return: MemberName or None
        """
        first_letter = name.last_name[0].lower()
        if self._index.get(first_letter, None) is None:
            return None
        for n in self._index[first_letter]:
            if isinstance(n, MemberName):
                if n == name:
                    return n
            else:
                if n[0] == name:
                    return n
        return None
