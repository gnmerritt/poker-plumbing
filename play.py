import argparse
import sys

from twisted.internet import reactor
import ConfigParser

from pipes.connector import MatchPlayer

parser = argparse.ArgumentParser(description="connect to a casino")
parser.add_argument('--key', help="secret key for your bot")
parser.add_argument("--runtime", help="path to your bot's runtime")
parser.add_argument("--games", help="number of games to play before quitting",
                    type=int)

Config = ConfigParser.ConfigParser()
Config.read('config.ini')


def get(param):
    return Config.get('Poker', param)


class Server(object):
    def __init__(self):
        self.api = get('api')

    def __repr__(self):
        return "Server<{}>".format(self.api)


class Bot(object):
    def __init__(self, args):
        if args.key:
            self.key = args.key
        else:
            self.key = get('key')
        if args.runtime:
            self.runtime = args.runtime
        else:
            self.runtime = get('runtime')
        self.runtime = self.runtime.split(" ")

    def __repr__(self):
        return "Bot<{} || {}>".format(
            self.key, self.runtime)


class GameCounter(object):
    def __init__(self, player, args):
        self.player = player
        self.played = 0
        self.games_wanted = args.games if args.games else int(get('games'))

    def play_or_quit(self):
        if self.played > self.games_wanted:
            reactor.stop()
        else:
            self.played += 1
            print "Playing game #{} of {}".format(
                self.played, self.games_wanted
            )
            self.player.play(self.play_or_quit)


def main(args):
    server = Server()
    bot = Bot(args)
    player = MatchPlayer(server, bot)
    counter = GameCounter(player, args)
    reactor.callLater(0.5, counter.play_or_quit)
    reactor.run()


if __name__ == "__main__":
    args = parser.parse_args()
    print "got key= {}".format(args.key)
    print "got runtime ={}]".format(args.runtime)
    main(args)
