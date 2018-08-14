# # -*- coding: utf-8 -*-
"""

"""
import sys
import config
from multiprocessing import Process
import subprocess
SOLUTION = sys.argv[1] if len(sys.argv) > 1 else config.kline_interval


def do_kline(sym):
    cmd = '{0}{1}{2}{3}'.format('python kcandle.py ', SOLUTION, ' ', sym)
    print('--- cmd---' + cmd)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    print(pipe.read())
    print('finished to trigger https kline information')


# 取K线数据
def sync_kline():
    for sy in config.sylist:
        pdepth = Process(target=do_kline, args=(sy,))
        print('syncing kline information is triggered')
        pdepth.start()


if __name__ == '__main__':
    sync_kline()

