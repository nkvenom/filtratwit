#!/usr/bin/env python
# en el followlist van ids
from __future__ import print_function
from __future__ import unicode_literals
import codecs
from datetime import datetime
import json

from textwrap import TextWrapper
import optparse
import sys
import re

import tweepy
import unicodedata
from tuitelerias import get_auth


def is_emoji(cp):
    '''
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

    :param char: a pair of unichrs representing a surrogate, unicode astral plane
    :return: the number representing the unique character
    '''
    if len(char) != 2:
        return ord(char)
    return 0x10000 + (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00)


def get_surrogates(ascii_chrs):
    '''
    :param ascii_chrs: an ascii escaped UTF-8 text
    :return: a list of unichrs representing the founded in the astral plane
    '''
    chrs = re.findall(r'\\uD\w{3}\\uD\w{3}', ascii_chrs, flags=re.IGNORECASE | re.MULTILINE)

    return [codecs.decode(x, 'unicode_escape') for x in chrs]


def get_all_emojis(ascii_chrs):
    return [x for x in get_surrogates(ascii_chrs) if is_emoji(get_uniord(x))]


def sanitize(w):
    # Strip punctuation from the front
    while len(w) > 0 and not w[0].isalnum():
        w = w[1:]

    # String punctuation from the back
    while len(w) > 0 and not w[-1].isalnum():
        w = w[:-1]

    return w


class StreamWatcherListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
    tweets_file = None

    def __init__(self, f_name, lang=None, only_with_emojis=False):
        super(StreamWatcherListener, self).__init__()
        self.only_with_emojis = only_with_emojis
        self.lang = None
        if lang:
            self.lang = u'' + lang
            
        today = datetime.today()
        ctime = today.strftime('%Y%m%d-%H%M')
        print('init called at %s' % ctime)

        try:
            self.tweets_file = codecs.open('%s-%s.json' % (f_name, ctime), 'a', 'utf8')
        except IOError:
            print('Couldnt open file, exitos')
            exit()

    def on_data(self, data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """
        if 'in_reply_to_status_id' in data:
            status = data
            if self.on_status(status) is False:
                return False
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False

    def on_status(self, status):

        if self.only_with_emojis:
            emojis = get_all_emojis(status)
            if not emojis:
                return
            else:
                print(','.join(unicodedata.name(e, '-') for e in emojis))

        twj = json.loads(status)
        if self.lang is not None and twj['lang'] != self.lang:
            return
        try:
            self.tweets_file.write(status)

        except Exception as e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            print('Error found trying to parse the tweet {}'.format(e))

    def on_error(self, status_code):
        print('An error has occurred! Status code = %s' % status_code)
        return True  # keep stream alive

    def on_timeout(self):
        print('Snoozing Zzzzzz')

        self.tweets_file.close()
        exit()

    def clean_foo(self):
        self.tweets_file.close()


def main():
    stream = None
    try:
        # Prompt for login credentials and setup stream object
        my_auth = get_auth()

        p = optparse.OptionParser('prog -t "@foo, #baz, #bar" -f "user_id"')
        p.add_option('--only_with_emojis', '-w', action='store_true', default=False)
        p.add_option('--locs', default=None, help='4 coords representing a bounding box')
        p.add_option('--lang', default=None)
        p.add_option('--followlist', '-f')

        opts, args = p.parse_args()

        follow_list = track_list = []
        # if len(sys.argv) == 1:
        # print('Interactive mode enabled, if you want to call with options ')
        #     print('prog -t "@foo, #baz, #bar" -f "user_id"')
        #     follow_list = input('Users to follow (comma separated): ').strip()
        #     track_list = input('Keywords to track (comma separated): ').strip()
        # else:
        #     follow_list = opts.followlist
        #     track_list = opts.tracklist


        follow_list = opts.followlist
        track_list = args

        if follow_list:
            follow_list = [u.strip() for u in follow_list.split(',') if u != '']

        # if track_list:
        #    track_list = [k.strip() for k in track_list.split(',') if k != '']

        f_name = 'datwits'

        if track_list and len(track_list) > 0:
            f_name = track_list[0]
        elif follow_list and len(follow_list) > 0:
            f_name = follow_list[0]

        f_name = sanitize(f_name)
        stream = tweepy.Stream(my_auth, StreamWatcherListener(f_name, lang=opts.lang,
                                                              only_with_emojis=opts.only_with_emojis), timeout=None)

        print('follow_list= {}'.format(follow_list))
        print('track_list= {}'.format(track_list))

        locs = None
        if opts.locs:
            locs = [float(x) for x in opts.locs.split(',')]

        stream.filter(follow=follow_list, track=track_list, locations=locs)
    except KeyboardInterrupt:
        print('\nCtrl-C pressed, Goodbye!')


if __name__ == '__main__':
    main()
