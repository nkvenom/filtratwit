# coding=utf-8
import codecs
from collections import defaultdict
import simplejson as json
import sys
import tweepy


def get_auth(conf_path='auth_twitter.conf'):
    """ Lee los datos de autenticación de un archivo JSON """
    with open(conf_path) as auth_f:
        auth_data = json.loads(auth_f.read())
        consumer_key = auth_data['consumer_key']
        consumer_secret = auth_data['consumer_secret']

        access_token = auth_data['access_token']
        access_token_secret = auth_data['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

    return auth

