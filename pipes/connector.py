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
            to_join = game.first_active()
        except URLError as e:
            print "Whoops, looks like the server is down. Exiting."
            print "saw {}".format(e)
            sys.exit()
        if to_join:
            self.join(to_join)
        else:
            print "  no games found, sleeping..."
            time.sleep(10)

    def join(self, game):
        guid = game['guid']
        print "  joining {}".format(guid)
        player = PlayGame(game, self.bot)
        player.connect(guid)


class FindGame(object):
    def __init__(self, server, key):
        self.url = '{api}/api/matches?key={k}'.format(
            api=server.api, k=key
        )

    def first_active(self):
        print " polling {}".format(self.url)
        response = urlopen(self.url)
        data = str(response.read())
        parsed = json.loads(data)
        if parsed and parsed['data']:
            return parsed['data'][0]


class PlayGame(object):
    def __init__(self, game, bot):
        self.game = game
        self.bot = bot

    def connect(self, game_key):
        self.game = protocols.GameContainer(
            game_key, self.game, self.bot
        )
