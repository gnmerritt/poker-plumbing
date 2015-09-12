import datetime
import os.path


class GameLogger(object):
    """"Creates a timestamped log file containg the game activity"""
    def __init__(self, bot, game, log_dir):
        output = "{n}__{g}.log".format(n=bot['guid'], g=game['guid'])
        self.filename = os.path.join(log_dir, output)

    def __enter__(self):
        self.outf = open(self.filename, 'w')
        return self

    def __exit__(self, *args):
        self.outf.close()

    def write(self, line, prefix):
        now = datetime.datetime.utcnow()
        self.outf.write("[{d}] : {p} : {l}\n".format(d=now, p=prefix, l=line))

    def sent(self, line):
        self.write(line, "SENT")

    def received(self, line):
        self.write(line, "GOT")
