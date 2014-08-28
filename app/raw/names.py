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
            self.english_name = english_name
            self.last_name = last_name
            self.chinese_name = chinese_name
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
        pass

    def _parse_english_name(self, name):
        """
        Given an english full name, try to parse it into its constituent parts
        """
        title_re = ur'(?P<title>Mr|Mrs|Miss|Ms|Hon|Dr)'
        ename_re = ur'(?P<fname>[a-zA-Z]+)'
        lname_cap_re = ur'(?P<lname>[A-Z]+)'
        cname_re = ur'(?P<cname>[a-zA-Z-]+)'
        fully_qualified = ur'^(?P<title>Mr|Mrs|Miss|Ms|Hon|Dr)? ?(?P<fname>[a-zA-Z]+) (?P<lname>[A-Z]+) (?P<cname>[a-zA-Z-]+)?(, )?(?P<hon>[A-Z, ]+)?'
        match = re.match(fully_qualified, name)
        if match is not None:
            res = match.groupdict()
            self.english_name = proper(res['fname'])
            self.title = proper(res['title'])
            if res['hon'] is not None:
                self.honours = [xx.strip() for xx in res['hon'].split(',') if xx is not None]
            self.last_name = proper(res['lname'])
            self.chinese_name = proper(res['cname'])
        minimal = ur''
        reversed = ur''
        anglicized = ur''

    def _parse_chinese_name(self, name):
        """
        Given a chinese name, parse it into its constituent parts
        """
        pass

    @property
    def full_name(self):
        if self.is_english:
            if self.english_name is not None:
                return u'{} {}'.format(self.english_name, self.last_name)
            else:
                return u'{} {}'.format(self.chinese_name, self.last_name)
        else:
            return u'{}{}'.format(self.last_name, self.chinese_name)


class NameMatcher(object):
    pass