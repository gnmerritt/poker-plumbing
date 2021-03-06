# poker-plumbing
pipes and wires to get your poker bot talking to the world

[![Build Status](https://travis-ci.org/gnmerritt/poker-plumbing.svg?branch=master)](https://travis-ci.org/gnmerritt/poker-plumbing) [![codecov.io](http://codecov.io/github/gnmerritt/poker-plumbing/coverage.svg?branch=master)](http://codecov.io/github/gnmerritt/poker-plumbing?branch=master)


Setup
=====

Go to `https://casino.gnmerritt.net` and create an account. Add a new
bot to your account, and take note of its `passkey`. Add the key
and the command required to run your bot to your
[configuration file](config.ini).

Next, make sure you have the necessary python libraries installed:

```shell
python --version # should be 2.7 or higher
pip install -r requirements.txt
```

Finally, start your bot with:

```shell
python play.py
```

Logs will be streamed to [logs/](logs/) as the bot runs. Good luck!
