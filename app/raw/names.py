#!/usr/bin/python
# -*- coding: utf-8 -*-


def is_ascii(string):
    try:
        string.encode('ascii')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return False
    else:
        return True


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
            pass
        else:
            # Check for language, then call the relevant parser
            if is_ascii(full_name):
                self._parse_english_name(full_name)
            else:
                self._parse_chinese_name(full_name)
                self.is_english = False

    def __repr__(self):
        return u'<MemberName: {}>'.format(self.full_name)
        pass

    def __eq__(self, other):
        pass

    def _parse_english_name(self, name):
        pass

    def _parse_chinese_name(self, name):
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