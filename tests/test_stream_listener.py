import unittest
from stream_listener import *
from unittest.mock import patch

class TestStreamListener(unittest.TestCase):

    def test_on_error(self):
        ''' Passing error message to validate on_error method '''
        self.assertFalse(StreamListener.on_error(None, 'Stream encountered 403 forbidden'))

    @patch('builtins.print')
    def test_on_data(self, mock_print):
        '''
        Using mock_print to assert on_data method as it does not return any value.
        Validating what on_data prints againt expected assert
        data.txt file has sample tweet data in json format
        :param mock_print:
        '''
        with open("data.txt", "r") as text_file:
            data = text_file.read()
        StreamListener.on_data(None, data)
        mock_print.assert_called_with('not related event')

if __name__ == '__main__':
    unittest.main()
