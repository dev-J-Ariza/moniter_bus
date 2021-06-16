import unittest

from moniter_bus import api


class TestApi(unittest.TestCase):
    def test_all_busses(self):
        r = api.get_all_busses()
        self.assertIsNotNone(r)

