# coding=utf-8
import codecs
from collections import defaultdict
import simplejson as json
import sys
import tweepy


def get_auth():
    """ Lee los datos de autenticación de un archivo JSON """
    with open('auth_twitter.conf') as auth_f:
        auth_data = json.loads(auth_f.read())
        consumer_key = auth_data['consumer_key']
        consumer_secret = auth_data['consumer_secret']

        access_token = auth_data['access_token']
        access_token_secret = auth_data['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

    return auth


def get_users(f_name='filtered_users_2.json'):
    """ Extrae unicamente el json que corresponde a los usuarios del archivo de twitts """
    f = codecs.open(f_name, 'r', 'utf-8')
    counts = defaultdict(int)
    users = {}

    # line number
    ln = 0
    for line in f:
        try:
            ln += 1
            user = json.loads(line)
            u_name = user[u'screen_name']
            counts[u_name] += 1

            if not user['id'] in users:
                users[user['id']] = user
        except:
            print "Unexpected error: %s, at line %d" % (sys.exc_info()[0], ln)

    return users


def sort_users_file():
    users = get_users()
    user_list = sorted(users.values(), key=lambda user: user['id'])
    for v in user_list[:10]:
        print "%d[%s]: %s" % (v['id'], v['screen_name'], v['description'])
    out = codecs.open('filtered_users_2.json', 'w', 'utf-8')
    for u in user_list:
        out.write("%s\n" % json.dumps(u))
    out.close()

if __name__ == '__main__':
    my_auth = get_auth()