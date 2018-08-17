from gevent import monkey

monkey.patch_all()
import gevent
from kcandle import SyncMDCandle
from candle import SyncCandle
import config


def run_task():
    greenlets = []
    for sy in config.sylist:
        try:
            greenlets.append(gevent.spawn(SyncCandle().run, 'M1', sy))
            greenlets.append(gevent.spawn(SyncMDCandle().run, 'M1', sy))
        except Exception as e:
            print(e)
    gevent.joinall(greenlets)


if __name__ == '__main__':
    # print(sys.argv[0])
    run_task()
