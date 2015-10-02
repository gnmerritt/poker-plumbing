class MockServer(object):
    api = "apiUrl"


class MockLogger(object):
    def received(self, line):
        self.last_received = line

    def sent(self, line):
        self.last_sent = line

    def debug(self, line):
        self.last_debug = line

    def done(self):
        self.finished = True

class MockFactory(object):
    def __init__(self):
        self.bot = MockBot()
        self.logger = MockLogger()

    def on_finish(self):
        pass


class MockProcess(object):
    def kill(self):
        self.killed = True

    def tell(self, line):
        self.last_told = line


class MockBot(object):
    key = "bot_key"

    def register(self, protocol):
        self.registered = True

    def login(self):
        self.logged_in = True
        return "login"


class MockTransport(object):
    def signalProcess(self, signal):
        self.signal = signal

    def loseConnection(self):
        self.lost_connection = True

    def write(self, line):
        self.last_line = line
