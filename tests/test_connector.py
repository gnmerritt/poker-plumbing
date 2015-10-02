try:
    from urllib.request import URLError
except ImportError:
    from urllib2 import URLError
import unittest

from pipes.connector import FindGame
from mocks import MockServer


class FindGameTest(unittest.TestCase):
    def setUp(self):
        self.finder = FindGame(MockServer, "myKey")

    def test_url(self):
        self.assertEqual(self.finder.url, "apiUrl/api/matches?key=myKey")

    def fake_urlopen(self, url):
        def fake():
            pass

        def read():
            return '{"data":[7,0,0]}'
        fake.read = read
        return fake

    def test_first_active(self):
        self.finder.urlopen = self.fake_urlopen
        found = self.finder.first_active()
        self.assertEqual(7, found)

    def exploding_urlopen(self, url):
        raise URLError("BOOM")

    def test_first_active_down(self):
        self.finder.urlopen = self.exploding_urlopen
        found = self.finder.first_active()
        self.assertFalse(found)
