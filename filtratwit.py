#!/usr/bin/env python
# en el followlist van ids
from __future__ import print_function
from __future__ import unicode_literals
import codecs
from datetime import datetime
import json

from textwrap import TextWrapper
import argparse
from argparse import RawDescriptionHelpFormatter
import os.path
import re

import tweepy
import unicodedata
from tuitelerias import get_auth

import text_utils as tu

class StreamWatcherListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
    tweets_file = None

    def __init__(self, f_name, create_dir=True, langs=None, only_with_emojis=False):
        super(StreamWatcherListener, self).__init__()
        self.only_with_emojis = only_with_emojis
        self.langs = None

        today = datetime.today()
        ctime = today.strftime('%Y%m%d-%H%M')
        print('init called at %s' % ctime)

        filepath = '{}-{}.json'.format(f_name, ctime)
        if create_dir:
            if not os.path.exists(f_name):
                os.makedirs(f_name)
            filepath = '{}/{}-{}.json'.format(f_name, f_name, ctime)

        try:
            self.tweets_file = codecs.open(filepath, 'a', 'utf8')
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
            emojis = tu.get_all_emojis(status)
            if not emojis:
                return
            else:
                print(','.join(unicodedata.name(e, '-') for e in emojis))

        twj = json.loads(status)
        if self.langs is not None and twj['lang'] not in self.langs:
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


def main(argv=None):
    stream = None
    try:
        parser = argparse.ArgumentParser(description='Filter twits using the official API', formatter_class=RawDescriptionHelpFormatter)

        parser.add_argument('-w', '--only_with_emojis', default=False, action='store_true', help='Only store twitts that contains utf-8 emoji like characters')
        parser.add_argument('-c', '--locs', type=str, action='store', help='4 coords separated by commas, representing a bounding box', metavar='COORDINATES')
        parser.add_argument('-l', '--lang', type=str, action='store', help='filter in the client side by language, comma separated list of language codes, use \'und\' for undefined')
        parser.add_argument('-a','--auth', type=str, action='store', default='auth_twitter.conf', metavar='AUTHFILE')
        parser.add_argument('-f', '--followlist', type=str, help='IDs of specified twitter accounts separated by commas')
        parser.add_argument('tracklist', nargs='+', metavar='track_term', help='Space separated list of terms or hashtags to track')

        args = parser.parse_args()

        print("Using auth file={}".format(args.auth))
        my_auth = get_auth(args.auth)

        follow_list = []
        track_list = []

        follow_list = args.followlist
        track_list = args.tracklist

        if follow_list:
            follow_list = [u.strip() for u in follow_list.split(',') if u != '']


        f_name = 'datwits'

        if track_list and len(track_list) > 0:
            f_name = track_list[0]
        elif follow_list and len(follow_list) > 0:
            f_name = follow_list[0]

        langs=None
        if args.lang is not None:
            langs = [u'' + l.strip() for l in args.lang.split(',')]

        f_name = tu.sanitize(f_name)
        stream = tweepy.Stream(my_auth, StreamWatcherListener(f_name, langs=langs,
                                                              only_with_emojis=args.only_with_emojis), timeout=None)


        if follow_list:
            print('follow_list= {}'.format(follow_list))

        print('track_list= {}'.format(track_list))

        locs = None
        if args.locs:
            locs = [float(x) for x in args.locs.split(',')]

        stream.filter(follow=follow_list, track=track_list, locations=locs)
    except KeyboardInterrupt:
        print('\nCtrl-C pressed, Goodbye!')


if __name__ == '__main__':
    main()
