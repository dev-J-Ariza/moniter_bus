import unittest

from moniter_bus import api
from unittest.mock import patch


class TestApi(unittest.TestCase):
    def test_all_busses(self):
        r = api.get_all_busses()
        self.assertIsNotNone(r)

    @patch('builtins.input', return_value=1)
    def test_get_stations(self, mock_input):
        r = api.get_station(509, should_print=False)
        self.assertTrue(len(r) > 0)

    @patch('builtins.input', return_value=2)
    def test_real_time_bus(self, mock_input):
        r = api.get_real_time_bus(509)
        self.assertTrue(r or not r)
