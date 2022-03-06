import tweepy
from StreamListener import *
from Config import *

# Twitter authorization tokens
api_key = Config.twitter_api_key
api_key_secret = Config.twitter_api_key_secret
access_token = Config.twitter_access_token
access_token_secret = Config.twitter_access_token_secret

if __name__ == "__main__":
    stream_listener = StreamListener(api_key, api_key_secret, access_token, access_token_secret)
    stream_listener.filter(track=["Justin Bieber"])
