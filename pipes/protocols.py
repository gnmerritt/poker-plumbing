from twisted.internet import reactor
from twisted.protocols import basic
from twisted.internet.error import ReactorNotRunning
from twisted.internet.protocol import ClientFactory

from processes import PokerBotProcess


class PokerProtocol(basic.LineReceiver):
    """Client side of the poker protocol.
    Passes data from the server to the running poker bot, handles
    login from config options
    """
    delimiter = "\n"

    def banner(self, line):
        print "*" * 40
        print line
        print "*" * 40

    def connectionMade(self):
        self.banner("made connection to game server")
        self.process = self.factory.bot
        self.process.register(self)
        self.sendLine(self.process.login())

    def connectionLost(self, reason):
        self.banner("lost connection {}".format(reason))
        try:
            self.process.kill()
            reactor.callLater(1, self.factory.on_finish)
        except ReactorNotRunning:
            pass

    def lineReceived(self, line):
        self.factory.logger.received(line)
        self.process.tell(line)

    def tell_server(self, line):
        self.factory.logger.sent(line)
        self.sendLine(line)


class PokerProtocolFactory(ClientFactory):
    protocol = PokerProtocol

    def __init__(self, on_finish):
        self.on_finish = on_finish


class GameContainer(object):
    def __init__(self, game_key, server, bot, on_finish, logger):
        self.server = server
        self.factory = PokerProtocolFactory(on_finish)
        self.factory.logger = logger
        self.bot = PokerBotProcess(game_key, bot, self.on_connect, logger)
        self.factory.bot = self.bot
        reactor.spawnProcess(self.bot, bot.runtime[0], bot.runtime)

    def on_connect(self):
        server = self.server
        reactor.connectTCP(server['host'], server['port'], self.factory)
