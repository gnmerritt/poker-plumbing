from twisted.internet import reactor
from twisted.protocols import basic
from twisted.internet.protocol import ClientFactory


class LoadedBot(object):
    pass


class PokerProtocol(basic.LineReceiver):
    def connectionMade(self):
        print "made connection"
        self.delimiter = "\n"

    def connectionLost(self, reason):
        print "lost connection {}".format(reason)
        reactor.stop()

    def lineReceived(self, line):
        print "got line: {}".format(line)


class PokerProtocolFactory(ClientFactory):
    protocol = PokerProtocol

    def buildProtocol(self, address):
        return self.protocol()


class GameContainer(object):
    def __init__(self, server):
        reactor.connectTCP(server.host, server.port,
                           PokerProtocolFactory())
        reactor.run()
