try:
    from urllib.request import urlopen, URLError
except ImportError:
    from urllib2 import urlopen, URLError
import json

from twisted.internet import reactor

import protocols
from logger import GameLogger


class MatchPlayer(object):
    """
    Handles joining and playing games for a specified bot
    """
    def __init__(self, server, bot):
        self.server = server
        self.bot = bot

    def play(self, on_after_match):
        print "Finding a game for {b} on {s}".format(b=self.bot, s=self.server)
        game = FindGame(self.server, self.bot.key)
        to_join = game.first_active()
        if to_join:
            logger = GameLogger(self.bot.info.get('guid'),
                                to_join['guid'], self.bot.log_dir)
            self.join(to_join, logger, on_after_match)
        else:
            print "  no games found, sleeping..."
            reactor.callLater(10, on_after_match)

    def join(self, game, logger, on_after_match):
        guid = game['guid']
        print "  joining {}".format(guid)
        protocols.GameContainer(guid, game, self.bot, on_after_match, logger)


class FindGame(object):
    """
    Polls the API and provides a dictionary representing the first active game
    """
    def __init__(self, server, key):
        self.url = '{api}/api/matches?key={k}'.format(api=server.api, k=key)
        self.urlopen = urlopen

    def first_active(self):
        print " polling {}".format(self.url)
        try:
            response = self.urlopen(self.url)
            data = str(response.read())
            parsed = json.loads(data)
            if parsed and parsed['data']:
                return parsed['data'][0]
        except URLError:
            return None
