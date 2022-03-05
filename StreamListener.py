import tweepy
import json
import string
from tweepy.models import Status
from textblob import TextBlob
from nltk.corpus import wordnet
from TweetsProcessor import *

class StreamListener(tweepy.Stream):

    tweets_processor = TweetsProcessor()

    ''' Overriding this method to stop handling all events.
        We need to process only when users post tweets'''
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if "in_reply_to_status_id" in data:
            status = Status.parse(None, data)
            return self.on_status(status)
        print('not related event')

    '''overriding this method to print status instead of logging'''
    def on_status(self, status):
        text = getattr(status,'text')
        tweet = {"id_str": getattr(status,'id_str'), "text": text, "created_at": getattr(status,'created_at')}
        print(tweet)
        StreamListener.tweets_processor.filter_tweets(tweet)

    '''Overriding this method for custom error handling.
       disconnect when 420 (rate limit exceeded) or 403 (forbidden)'''
    def on_error(self, status_code):
        if status_code == 420:
            return False
        if status_code == 403:
            return False