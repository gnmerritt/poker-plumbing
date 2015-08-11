import argparse
import ConfigParser
from pipes.connector import MatchPlayer

parser = argparse.ArgumentParser(description="connect to a casino")
parser.add_argument('--key', help="secret key for your bot")
parser.add_argument("--runtime", help="path to your bot's runtime")
parser.add_argument("--games", help="number of games to play before quitting")

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


def main(args):
    server = Server()
    bot = Bot(args)

    player = MatchPlayer(server, bot)
    if args.games:
        for i in xrange(args.games):
            player.play
    else:
        while True:
            player.play()


if __name__ == "__main__":
    args = parser.parse_args()
    print "got key= {}".format(args.key)
    print "got runtime ={}]".format(args.runtime)
    main(args)
