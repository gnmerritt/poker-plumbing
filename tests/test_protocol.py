import unittest
from pipes.protocols import PokerProtocol
from mocks import MockFactory, MockProcess


class PokerProtocolTest(unittest.TestCase):
    def send_line(self, line):
        self.last_line = line

    def setUp(self):
        self.protocol = PokerProtocol()
        self.protocol.sendLine = self.send_line
        self.protocol.process = MockProcess()
        self.protocol.factory = MockFactory()

    def test_connection_made(self):
        self.protocol.connectionMade()
        self.assertTrue(self.protocol.factory.bot.logged_in)
        self.assertTrue(self.protocol.factory.bot.registered)
        self.assertEqual(self.last_line, "login")

    def test_connection_lost(self):
        self.protocol.connectionLost("explode")
        self.assertTrue(self.protocol.process.killed)

    def test_line_received(self):
        p = self.protocol
        p.lineReceived("a line")
        self.assertEqual("a line", p.process.last_told)
        self.assertEqual("a line", p.factory.logger.last_received)

    def test_tell_server(self):
        p = self.protocol
        p.tell_server("hello")
        self.assertEqual("hello", self.last_line)
        self.assertEqual("hello", p.factory.logger.last_sent)
