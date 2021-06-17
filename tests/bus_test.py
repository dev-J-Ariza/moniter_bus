from mock import patch
from moniter_bus import bus
import unittest


class TestFoo(unittest.TestCase):

    @patch('moniter_bus.bus.get_station')
    def test_foo_case(self, mock_bar):
        bus.get_station(509)
        self.assertTrue(mock_bar.called)
        self.assertIsNotNone(mock_bar.call_args[0][0])
