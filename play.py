import ConfigParser
from pipes.connector import MatchPlayer


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
    def __init__(self):
        self.key = get('key')
        self.runtime = get('runtime').split(" ")

    def __repr__(self):
        return "Bot<{} || {}>".format(
            self.key, self.runtime)


def main():
    server = Server()
    bot = Bot()

    player = MatchPlayer(server, bot)
    player.play()


if __name__ == "__main__":
    main()
