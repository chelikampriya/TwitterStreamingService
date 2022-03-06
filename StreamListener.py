import tweepy
import json
import string
from tweepy.models import Status
from textblob import TextBlob
from nltk.corpus import wordnet
from TweetsProcessor import *

class StreamListener(tweepy.Stream):

    tweets_processor = TweetsProcessor()

    def on_data(self, raw_data):
        ''' Overriding this method to stop handling all events.
                We need to process only when users post tweets
                :param raw_data: raw_data from twitter event'''
        data = json.loads(raw_data)
        if "in_reply_to_status_id" in data:
            status = Status.parse(None, data)
            self.on_status(status)
        if "errors" in data:
            errors = data["errors"]
            if not self.on_errors(errors):
                self.session.close()
        print('not related event')

    def on_status(self, status):
        '''overriding this method to call TweetsProcessor methods
            :param status: parsed status from tweet data'''
        text = getattr(status,'text')
        tweet = {"id_str": getattr(status,'id_str'), "text": text, "created_at": getattr(status,'created_at')}
        print(tweet)
        StreamListener.tweets_processor.filter_tweets(tweet)

    def on_error(self, status_code):
        '''Overriding this method for custom error handling.
               disconnect when 420 (rate limit exceeded) or 403 (forbidden)
               :param status_code: error text containing error code
               :return: bool when 420 or 403 error'''
        if status_code == 420:
            return False
        if status_code == 403:
            return False