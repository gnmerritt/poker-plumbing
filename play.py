import argparse
import requests

from twisted.internet import reactor
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from pipes.connector import MatchPlayer

parser = argparse.ArgumentParser(description="connect to a casino")
parser.add_argument('--key', help="secret key for your bot")
parser.add_argument("--runtime", help="path to your bot's runtime")
parser.add_argument("--games", help="number of games to play before quitting",
                    type=int)

Config = configparser.ConfigParser()
Config.read('config.ini')


def get(param):
    return Config.get('Poker', param)


class Server(object):
    def __init__(self):
        self.api = get('api')

    def __repr__(self):
        return "Server<{}>".format(self.api)


class Bot(object):
    def __init__(self, server, args):
        self.server = server
        if args.key:
            self.key = args.key
        else:
            self.key = get('key')
        if args.runtime:
            self.runtime = args.runtime
        else:
            self.runtime = get('runtime')
        self.runtime = self.runtime.split(" ")
        self.log_dir = get('log_dir')
        self.get_info()

    def get_info(self):
        r = requests.get("{}/api/bot/{}".format(self.server.api, self.key))
        bot_json = r.json()
        if bot_json and bot_json.get('bot'):
            self.info = bot_json.get('bot')

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
            print("Playing game #{} of {}".format(
                self.played, self.games_wanted
            ))
            self.player.play(self.play_or_quit)


def print_banner(bot_info):
    print("\n\nLogin succeeded. You are playing as:")
    print("  '{n}' (key={k}) ".format(
        n=bot_info.get('name'), k=bot_info.get('key')))
    print("  Currently ranked #{r} with a skill of {s}".format(
        r=bot_info.get('rank'), s=bot_info.get('skill')))
    print("\n")


def main(args):
    server = Server()
    bot = Bot(server, args)
    if bot.info:
        print_banner(bot.info)
        player = MatchPlayer(server, bot)
        counter = GameCounter(player, args)
        reactor.callLater(0.5, counter.play_or_quit)
        reactor.run()
    else:
        print("Couldn't find your bot - please check the key and try again")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
