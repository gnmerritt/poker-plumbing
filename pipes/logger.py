import datetime
import os


class GameLogger(object):
    """"Creates a timestamped log file containg the game activity"""
    def __init__(self, bot_key, game_key, log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        output = "{n}__{g}.log".format(n=bot_key, g=game_key)
        self.filename = os.path.join(log_dir, output)
        self.outf = open(self.filename, 'w')
        print "Writing game logs to '{}'".format(self.filename)

    def done(self):
        self.outf.close()

    def write(self, line, prefix):
        now = datetime.datetime.utcnow()
        self.outf.write("[{d}] : {p} : {l}\n".format(d=now, p=prefix, l=line))

    def sent(self, line):
        self.write(line, "SENT")

    def received(self, line):
        self.write(line, "GOT")

    def debug(self, line):
        self.write(line, "DEBUG")
