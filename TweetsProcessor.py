import tweepy
import json
import string
from tweepy.models import Status
from textblob import TextBlob
from nltk.corpus import wordnet
import redshift_connector
from Config import *

class TweetsProcessor():
    '''Opening Redshift Connection'''
    conn = redshift_connector.connect(
        host=Config.redshift_host,
        port=5439,
        database=Config.redshift_database,
        user=Config.redshift_user,
        password=Config.redshift_password,
        tcp_keepalive=True
    )

    def get_synonyms(self, word):
        '''Method to get synonyms of the word given
          :param word: string to get synonyms for
          :return: list of synonyms for given word'''
        syn = set()
        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                syn.add(lemma.name())
        syn.add('song')
        syn.add('listen')
        syn.add('melody')
        print(syn)
        return list(syn)

    synonyms = get_synonyms(None, word = "Music")

    def translate_to_english(self, text):
        '''Method to translate text to English
           :param text: string to translate
           :return: string after translating to English'''
        blob = TextBlob(text)
        try:
            blob = blob.translate(to='en')
        except:
            pass
        return str(blob)

    def store_in_redshift(self, tweet, table_name):
        '''Method to execute the insert command to store data in Redshift
           :param tweet: dictionary containing tweet data. keys expected: id_str, text, created_at
           :param table_name: atring specifying redshift table name to insert tweet data passed'''
        comm = 'INSERT INTO dev.public.{table} (id_str,text,translated,created_at) VALUES (\'{id_str}\',\'{text}\',\'{translated}\',\'{created_at}\');'
        comm = comm.format(table = table_name, id_str = tweet['id_str'],text = str(tweet['text']).replace('"', r'\"').replace('\'', r'\''), translated = str(tweet['translated']).replace('"', r'\"').replace('\'', r'\''), created_at = tweet['created_at'])
        with TweetsProcessor.conn.cursor() as cursor:
            cursor.execute(comm)
            TweetsProcessor.conn.commit()
            print(comm)

    def filter_tweets(self, tweet):
        '''Method to process tweets, calls other methods as needed
           :param tweet: dictionary containing tweet data. keys expected: id_str, text, created_at'''
        print('in processor: {}'.format(tweet))
        translated = TweetsProcessor.translate_to_english(None, text = tweet['text'])
        print(translated)
        tweet["translated"] = translated
        try:
            TweetsProcessor.store_in_redshift(None, tweet = tweet, table_name = 'tweets')
        except:
            print('error')
            tweet["text"] = translated
            TweetsProcessor.store_in_redshift(None, tweet = tweet, table_name = 'tweets')
        if any(w in translated.lower() for w in TweetsProcessor.synonyms):
            print('related tweet')
            TweetsProcessor.store_in_redshift(None, tweet=tweet, table_name='tweets_music')
        print(translated)

