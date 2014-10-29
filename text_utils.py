from __future__ import print_function
from __future__ import unicode_literals
import codecs

import re


def is_emoji(cp):
    '''
    This function identifies emojis, cp is assumed to be a 32bit character

    :param cp: unicode codepoint
    :return: True if is a emoju
    '''
    # new in unicode 7
    if 0x1F300 <= cp <= 0x1F5FF:
        return True
    # other emoticons
    elif 0x1F600 <= cp <= 0x1F640F:
        return True
    elif 0x2600 <= cp <= 0x26FF:
        return True
    elif 0x2700 <= cp <= 0x27BF:
        return True


def get_uniord(char):
    '''
    Convert a pair of 16bit chars into a single 32bit encoded unicode char

    :param char: a pair of unichrs representing a surrogate, unicode astral plane
    :return: the number representing the unique character
    '''
    if len(char) != 2:
        return ord(char)
    return 0x10000 + (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00)



def get_surrogates(ascii_chrs):
    '''
    In the resulting twitter JSON emojis are encoded as a pair of ascii encoded utf-8 characters
    Ex: '\ud83d\ude31' 'is FACE SCREAMING IN FEAR' or (U+1F631)
    :param ascii_chrs: an ascii escaped UTF-8 text or a utf-8 string
    :return: a list of unichrs representing the ones founded in the astral plane
    '''

    # If we find an ascii encode surrogate pair the convert to unicode
    chrs = re.findall(r'\\uD\w{3}\\uD\w{3}', ascii_chrs, flags=re.IGNORECASE | re.MULTILINE)
    if chrs:
        chrs = [codecs.decode(x, 'unicode_escape') for x in chrs]
    else:
        # If ascii encoded surrogetes are not founded in the text
        # returns bytes so match against bytes and the convert the result again to utf8
        ascii_chrs = ascii_chrs.encode('unicode_escape')
        chrs = re.findall(b'\\\\U000\w{5}', ascii_chrs, re.MULTILINE)
        chrs = [ch.decode('unicode_escape') for ch in chrs]

    return chrs

def to_surrogates(unich):
    '''
    Returns an ascii surrogate pair given an already encoded unicode character
    :param unich:
    :return:
    '''
    return codecs.encode(unich, 'unicode_escape')

def get_all_emojis(ascii_chrs):
    '''
    Get all emojis contained in the ascii encoded utf8 text
    :param ascii_chrs:
    :return:
    '''
    return [x for x in get_surrogates(ascii_chrs) if is_emoji(get_uniord(x))]


def sanitize(w):
    # Strip punctuation from the front
    while len(w) > 0 and not w[0].isalnum():
        w = w[1:]

    # String punctuation from the back
    while len(w) > 0 and not w[-1].isalnum():
        w = w[:-1]

    return w