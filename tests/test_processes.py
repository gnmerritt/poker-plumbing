import unittest

from mocks import MockBot, MockLogger, MockTransport

from pipes.processes import PokerBotProcess


class BotProcessTest(unittest.TestCase):
    is_connected = False

    def connected(self):
        self.is_connected = True

    def setUp(self):
        self.logger = MockLogger()
        self.bot = PokerBotProcess(
            "game_key", MockBot(), self.connected, self.logger)
        self.bot.transport = MockTransport()

    def test_connection_made(self):
        self.assertFalse(self.is_connected)
        self.bot.connectionMade()
        self.assertTrue(self.is_connected)

    def test_err_received(self):
        self.bot.errReceived("bang")
        self.assertEqual(self.logger.last_debug, "bang")

    def test_login(self):
        login_str = self.bot.login()
        self.assertEqual(login_str, "!login game_key bot_key")

    def test_register(self):
        self.bot.register("foo")
        self.assertEqual(self.bot.connection, "foo")

    def test_kill(self):
        b = self.bot
        b.kill()
        self.assertEqual(b.transport.signal, "KILL")
        self.assertTrue(b.transport.lost_connection)
        self.assertTrue(self.logger.finished)
