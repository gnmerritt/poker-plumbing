from twisted.internet import protocol
from twisted.python import log


class PokerBotProcess(protocol.ProcessProtocol):
    def __init__(self, game_key, bot, on_connect, logger):
        self.game = game_key
        self.bot = bot
        self.on_connect = on_connect
        self.logger = logger

    def connectionMade(self):
        self.on_connect()

    def outReceived(self, data):
        self.connection.tell_server(data)

    def errReceived(self, data):
        for line in data.split("\n"):
            self.logger.debug(line)

    def login(self):
        print("  logging in...")
        return "!login {} {}".format(self.game, self.bot.key)

    def tell(self, line):
        try:
            self.transport.write(line + "\n")
        except:
            log.err()

    def kill(self):
        self.transport.signalProcess('KILL')
        self.transport.loseConnection()
        self.logger.done()

    def register(self, connection):
        print("Connection registered")
        self.connection = connection
