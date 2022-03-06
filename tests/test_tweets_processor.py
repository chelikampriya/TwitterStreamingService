import unittest
from tweets_processor import *

class TestTweetsProcessor(unittest.TestCase):

    def test_redshift_connection(self):
        '''Passing a twitter id (id_str) to redshift and querying for text and asserting it with expected text.
           Main goal is to validate redshift connection here.'''
        tweet_id = '1500325221710299138'
        tweet_text = "\"idc Justin Bieber music is therapeutic\""
        select_command = 'SELECT text FROM "dev"."public"."tweets_music" where id_str = {};'
        with TweetsProcessor.conn.cursor() as cur:
            cur.execute(select_command.format(tweet_id))
            response = ''.join(cur.fetchall()[0])
        print(response)
        self.assertEqual(response, tweet_text)

if __name__ == '__main__':
    unittest.main()
