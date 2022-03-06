# TwitterStreamingService
Establish Twitter streaming service to read filtered tweets and store to AWS Redshift

On main.py:
a.	Creating an instance of StreamListener class by passing twitter credentials.
b.	Calling Twitter’s filter.json endpoint, giving he filter word “Justin Bieber”
c.	This created a streaming service and gets tweets from endpoint. 

On stream_listener.py
a.	Using tweepy Twitter API library.
b.	In this class, methods are created / overridden to receive tweet data, get attributes from tweet and call TweetsProcessor methods for processing data.   

On tweets_processor.py
a.	Using nltk.corpus’s wordnet to generate synonyms for ‘music’
b.	Using textblob for translating tweet text to English to distinguish between tweets having music related word and others.
c.	Using redshift_connector to connect to AWS redshift instance.
d.	In this class, methods are processing tweet data received, translating, comparing, and storing in Redshift. 

On configs.py: This file has twitter and aws redshift credentials.  

On test_stream_listener.py: 
a.	test_on_error: Passing error message to validate on_error method
b.	test_on_data: Using mock_print to assert on_data method as it does not return any value. Validating what on_data prints againt expected assert. data.txt file has sample tweet data in json format

On test_tweets_processor.py:
a.	test_redshift_connection: Passing a twitter id (id_str) to redshift and querying for text and asserting it with expected. Main goal is to validate redshift connection here.
