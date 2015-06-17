import sys
import subprocess as sp
from threading  import Thread

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


class LoadedBot(object):
    def __init__(self, game, bot):
        self.game = game
        self.bot = bot
        self.process = BotProcess(bot.runtime)

    def login(self):
        print "  logging in..."
        return "!login {} {}".format(self.game, self.bot.key)

    def tell(self, line):
        try:
            self.process.put(line)
        except IOError as e:
            print "Error talking to bot process: {}" \
              .format(e)

    def ask(self):
        return self.process.get()

    def kill(self):
        self.process.shutdown()


class BotProcess(object):
    def __init__(self, source_file, print_bot_output=True):
        self.exploded = False
        self.process = self.process_out = None
        # TODO: fix this
        output = sys.stderr if print_bot_output else sp.PIPE
        try:
            self.process = p = sp.Popen([source_file],
                                        stdin=sp.PIPE,
                                        stdout=sp.PIPE,
                                        stderr=output,
                                        bufsize=1,
                                        close_fds=ON_POSIX)
            self.process_out = Queue()
            t = Thread(target=enqueue_output, args=(p.stdout, self.process_out))
            t.daemon = True # thread dies with the program
            t.start()
        except OSError as e:
            print "bot file doesn't exist, skipping {}".format(repr(e))
            self.exploded = True
        # TODO: more error catching probably

    def put(self, line):
        if self.process:
            self.process.stdin.write(line)
            self.process.stdin.write('\n')
            self.process.stdin.flush()

    def get(self, timeout=1):
        """Gets the most recent line"""
        line = None
        try:
            line = self.process_out.get(timeout=timeout)
        except Empty:
            pass
        return line

    def shutdown(self):
        if self.process:
            self.process.kill()
