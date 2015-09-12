import os.path
import unittest
import shutil
import tempfile

from pipes.logger import GameLogger


class LoggerTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.bot = 'BOT_GUID'
        self.game = 'GAME_GUID'

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_filenames(self):
        logger = GameLogger(self.bot, self.game, self.dir)

        self.assertTrue(os.path.exists(logger.filename))
        self.assertIn(self.bot, logger.filename)
        self.assertIn(self.game, logger.filename)
        self.assertTrue(logger.filename.endswith(".log"))

        # file shouldn't disappear when resource closes
        logger.done()
        self.assertTrue(os.path.exists(logger.filename))

    def test_writes(self):
        logger = GameLogger(self.bot, self.game, self.dir)
        logger.sent("SENT LINE")
        logger.received("RECEIVED LINE")
        logger.sent("SENT ANOTHER")
        logger.done()

        with open(logger.filename, "r") as logfile:
            data = logfile.readlines()
            self.assertEqual(len(data), 3)
            self.assertIn("SENT LINE", data[0])
            self.assertIn("RECEIVED LINE", data[1])
            self.assertIn("SENT ANOTHER", data[2])
