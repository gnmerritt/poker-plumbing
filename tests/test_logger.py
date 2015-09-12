import os.path
import unittest
import shutil
import tempfile

from pipes.logger import GameLogger


class LoggerTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.bot = {'guid': 'BOT_GUID'}
        self.game = {'guid': 'GAME_GUID'}

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_filenames(self):
        with GameLogger(self.bot, self.game, self.dir) as logger:
            self.assertTrue(os.path.exists(logger.filename))
            self.assertIn(self.bot['guid'], logger.filename)
            self.assertIn(self.game['guid'], logger.filename)
            self.assertTrue(logger.filename.endswith(".log"))
        # file shouldn't disappear when resource closes
        self.assertTrue(os.path.exists(logger.filename))

    def test_writes(self):
        with GameLogger(self.bot, self.game, self.dir) as logger:
            logger.sent("SENT LINE")
            logger.received("RECEIVED LINE")
            logger.sent("SENT ANOTHER")
            filename = logger.filename
        with open(filename, "r") as logfile:
            data = logfile.readlines()
            self.assertEqual(len(data), 3)
            self.assertIn("SENT LINE", data[0])
            self.assertIn("RECEIVED LINE", data[1])
            self.assertIn("SENT ANOTHER", data[2])
