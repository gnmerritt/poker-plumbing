from twisted.internet import reactor
from twisted.protocols import basic
from twisted.internet.error import ReactorNotRunning
from twisted.internet.protocol import ClientFactory

from processes import LoadedBot


class PokerProtocol(basic.LineReceiver):
    delimiter = "\n"

    def connectionMade(self):
        print "  made connection to game server"
        self.sendLine(self.bot.login())

    def connectionLost(self, reason):
        print "  lost connection {}".format(reason)
        try:
            self.bot.kill()
            reactor.stop()
        except ReactorNotRunning:
            pass

    def lineReceived(self, line):
        self.bot.tell(line)


class PokerProtocolFactory(ClientFactory):
    protocol = PokerProtocol

    def buildProtocol(self, address):
        new_protocol = self.protocol()
        new_protocol.bot = self.container.bot
        return new_protocol


class GameContainer(object):
    def __init__(self, game_key, server, bot):
        self.bot = LoadedBot(game_key, bot)
        factory = PokerProtocolFactory()
        factory.container = self
        reactor.connectTCP(server.host, server.port,
                           factory)
        reactor.run()
