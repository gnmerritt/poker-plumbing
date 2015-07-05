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
            reactor.stop()
        except ReactorNotRunning:
            pass

    def lineReceived(self, line):
        if line.startswith("!"):
            print line
        print "<<< {}".format(line)
        self.process.tell(line)

    def tell_server(self, line):
        print ">>> {}".format(line)
        self.sendLine(line)


class PokerProtocolFactory(ClientFactory):
    protocol = PokerProtocol


class GameContainer(object):
    def __init__(self, game_key, server, bot):
        factory = PokerProtocolFactory()

        def on_connect():
            reactor.connectTCP(server['host'], server['port'],
                               factory)

        self.bot = PokerBotProcess(game_key, bot, on_connect)
        factory.bot = self.bot
        reactor.spawnProcess(self.bot, bot.runtime[0], bot.runtime)
        reactor.run()
