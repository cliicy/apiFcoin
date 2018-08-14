# # -*- coding: utf-8 -*-
"""
运行此文件的方式： python dokline.py 默认一分钟
                   python dokline.py D1 指定取距离当前运行时间1天或者24小时的数据 一次请求返回102天的数据
                   python dokline.py M1ALL 要指定每天凌晨启动 获取距离凌晨前24小时的数据：自己设定limite
"""
import sys
import config
from multiprocessing import Process
import subprocess
SOLUTION = sys.argv[1] if len(sys.argv) > 1 else config.default_solution


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
        # print('syncing kline information is triggered')
        pdepth.start()


def do_allkline(sym):
    cmd = '{0}{1}{2}{3}'.format('python candle.py ', config.default_solution, ' ', sym)
    print('--- cmd---' + cmd)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    print(pipe.read())
    print('finished to trigger https kline information')


# 取K线数据 最新1440条
def sync_M1allkline():
    for sy in config.sylist:
        pdepth = Process(target=do_allkline, args=(sy,))
        # print('syncing kline information is triggered')
        pdepth.start()


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == 'M1ALL':
        sync_M1allkline()
    else:
        sync_kline()




