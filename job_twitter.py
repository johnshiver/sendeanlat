# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
import json
import time
import datetime
from tweepy import OAuthHandler
from tweepy import Stream
from header import consumer_key, consumer_secret, access_token, access_token_secret


from models import db, Tweet


cross_reference = [u'tren',
                   u'otobüs',
                   u'minibus',
                   u'tramvay',
                   u'vapur',
                   u'dolmuş',
                   u'araba',
                   u'taxi'
                   u'bayan-yanı',
                   u'metro',
                   u'bus',
                   u'tramway',
                   u'ferry',
                   u'train',
                   u'car']


simple_cache = {}


def fix_unicode(text):
    return text.encode(encoding='UTF-8')


def fix_140(text):
    xml_dict = {';': '', '&lt': '<', '&amp': '&', '&gt': '>', '&quot': '"', '&apos': '\''}
    for key, value in xml_dict.iteritems():
        text = text.replace(key, value)
    return text


def fix_text(text):
    text = text.replace("'", "")
    text = fix_140(text)
    return fix_unicode(text)


def fix_lists(hashtags):
    str1 = '{'
    hashtags = ", ".join(hashtags)
    str1 += hashtags
    str1 += '}'
    return fix_unicode(str1)


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):

        json_data = json.loads(data)

        text = json_data.get('text', None)
        # if text:
        #     text = fix_text(text)
        hashtags = None
        try:
            hashtags = json_data.get('entities', None).get('hashtags', None)[0].get('text')
            hashtags = fix_text(hashtags)
        except Exception as e:
            print e
        try:
            screen_name = json_data.get('user',  None).get('screen_name', None)
            screen_name = fix_text(screen_name)
        except Exception as e:
            screen_name = 'None'

        if hashtags:
            for i in cross_reference:
                if i in text:
                    print '*' * 30
                    print "YES IT WORKED WOWOOWOWO"
                    try:
                        tweet = Tweet(screen_name=screen_name, tweet=text, time=datetime.datetime.now(), hash_tag=hashtags, match_term=i)
                        # find_tweet = text.decode(encoding='UTF-8')
                        simple_cache[text] = 1
                        same_tweets = Tweet.query.filter_by(tweet=text).all()
                        if len(same_tweets) > 1:
                            break
                        db.session.add(tweet)
                        db.session.commit()
                        print "DB SUCCESS"
                        break
                    except Exception as e:
                        print "Yikes there was an error %s" % e
                        db.session.rollback()

    def on_error(self, status):
        error_counter = 0
        try:
            print 'Twitter stream error, status: {} '.format(status)
        except TypeError as x:
            print "-->Error logging status of... error...?: {}".format(x.args)
        if status == 420:
            time.sleep(15)
            error_counter += 1
            print 'There have been {} 420 errors'.format(error_counter)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    if stream:
        print "Successfully connected!"
    stream.filter(track=['sendeanlat'])
