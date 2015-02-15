# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
import json
import time
# import datetime
from tweepy import OAuthHandler
from tweepy import Stream
from header import consumer_key, consumer_secret, access_token, access_token_secret


from models import db, Tweet


cross_reference = ['tren',
                   'otobüs',
                   'minibus',
                   'tramvay',
                   'vapur',
                   'dolmuş',
                   'araba',
                   'taxi'
                   'bayan-yanı',
                   'metro',
                   'bus',
                   'tramway',
                   'ferry',
                   'train',
                   'car']


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
        try:
            hashtags = json_data.get('entities', None).get('hashtags', None)[0].get('text')
        except Exception as e:
            print e
        hashtags = fix_text(hashtags)
        text = fix_text(text)
        screen_name = json_data.get('user',  None).get('screen_name', None)
        screen_name = fix_text(screen_name)
        urls = [i['display_url'] for i in json_data.get('entities', None).get('urls', None)]
        urls = fix_lists(urls)
        # timestamp = str(datetime.datetime.now())

        # print "*"*40
        # print "Screen Name: {}".format(screen_name)
        # print "Text: {}".format(text)
        # print "URLs: {}".format(urls)

        # try:
        #     tweet = Tweet(screen_name=screen_name, text=text, timestamp=timestamp)
        #     db.session.add(tweet)
        #     db.session.commit()
        #     print "DB SUCCESS"
        # except Exception as e:
        #     import traceback; traceback.print_exc();
        # print "Yikes there was an error %s" % e
        for i in cross_reference:
            if i in text:
                print '*' * 30
                print "YES IT WORKED WOWOOWOWO"
                print i
                print "Text: {}".format(text)
                print "URLs: {}".format(urls)
                print '*' * 30
                break

        # text = fix_text(text)

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
