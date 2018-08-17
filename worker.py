from gevent import monkey

monkey.patch_all()
import gevent
from candle import SyncCandle
import config
import sys


def run_task():
    greenlets = []
    for sy in config.sylist:
        try:
            greenlets.append(gevent.spawn(SyncCandle().run, 'M1', sy))
        except Exception as e:
            print(e)
    gevent.joinall(greenlets)


if __name__ == '__main__':
    # print(sys.argv[0])
    run_task()
