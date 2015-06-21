import sys
try:
    from urllib.request import urlopen, URLError
except ImportError:
    from urllib2 import urlopen, URLError

import json
import time
import protocols


class MatchPlayer(object):
    def __init__(self, server, bot):
        self.server = server
        self.bot = bot

    def play(self):
        print "Finding a game for {b} on {s}".format(
            b=self.bot, s=self.server
        )
        game = FindGame(self.server, self.bot.key)
        try:
            guid = game.get_guid()
        except URLError:
            print "Whoops, looks like the server is down. Exiting."
            sys.exit()
        if guid:
            self.join(guid)
        else:
            print "  no games found, sleeping..."
            time.sleep(10)

    def join(self, guid):
        print "  joining {}".format(guid)
        player = PlayGame(self.server, self.bot)
        player.connect(guid)


class FindGame(object):
    def __init__(self, server, key):
        self.url = '{api}/api/matches?key={k}'.format(
            api=server.api, k=key
        )

    def get_guid(self):
        response = urlopen(self.url)
        data = str(response.read())
        parsed = json.loads(data)
        if parsed:
            # try to join the first active game
            game = parsed['data'][0]
            return game['guid']


class PlayGame(object):
    def __init__(self, server, bot):
        self.server = server
        self.bot = bot

    def connect(self, game_key):
        self.game = protocols.GameContainer(
            game_key, self.server, self.bot
        )
