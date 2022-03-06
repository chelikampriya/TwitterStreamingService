import unittest
from stream_listener import *
from unittest.mock import patch, call

class TestStreamListener(unittest.TestCase):

    def test_on_error(self):
        self.assertFalse(StreamListener.on_error(None, 'Stream encountered 403 forbidden'))

    @patch('builtins.print')
    def test_on_data(self, mock_print):
        with open("data.txt", "r") as text_file:
            data = text_file.read()
        StreamListener.on_data(None, data)
        mock_print.assert_called_with('not related event')

if __name__ == '__main__':
    unittest.main()
