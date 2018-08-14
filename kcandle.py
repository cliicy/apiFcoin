# # -*- coding: utf-8 -*-
"""

"""
from fcoin import Fcoin
from config import kline_interval
import os
import csv
import time
import json
import sys

fcoin = Fcoin()
fcoin.auth('key ', 'secret')
sDir = os.path.abspath(os.path.join(os.path.abspath('..'), '..', 'http_fcoin_data', 'kline'))
stime = time.strftime('%Y%m%d', time.localtime())


def start_kline():
    loop = 0
    while True:
        try:
            sync_kline()
            loop += 1
            print('获取kline第 %s 次' % loop)
        except Exception as error:
            print(error)
        if SOLUTION == 'M1':  # 1分 默认获得150条数据
            time.sleep(9000)  # 150*60
        elif SOLUTION == 'D1':  # 1天 默认传回102条数据
            time.sleep(6120)  # 102*60


# 取K线数据
def sync_kline():
    sdataDir = os.path.join(sDir, SOLUTION)
    # print(sdataDir)
    if not os.path.exists(sdataDir):
        os.makedirs(sdataDir)

    sTfile = '{0}_{1}_{2}'.format(stime, SYM, 'candle.txt')
    sTfilepath = os.path.join(sdataDir, sTfile)

    # save original data to csv
    sfile = '{0}_{1}_{2}'.format(stime, SYM, 'candle.csv')
    sfilepath = os.path.join(sdataDir, sfile)
    rdata = fcoin.get_candle(SOLUTION, SYM)  # 获取特定solution的kline数据
    candleinfo = rdata['data']
    # if solution = M1 = 1分钟线，   取150条数据
    # if solution = D1 = 1天线，   取102天的数据
    sflag = 'open'
    rFind = False
    print('单次获取的数据量：%s' % len(candleinfo))
    for ones in candleinfo:
        # print(ones)
        # 从服务器得到的数据中没有ts，只有id，根据文档要求，要把获取到数据的时间存入csv文件及数据库中
        ts = int(round(ones['id'] * 1000))
        ticks = int(round(time.time() * 1000))
        ones['id'] = ts
        kklist = []
        vvlist = []
        if os.path.exists(sfilepath):
            with open(sfilepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFind = sflag in first_line
        with open(sfilepath, 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            if rFind is True:
                additem2list(ticks, vvlist, SYM, SOLUTION, ones)
                w.writerow(vvlist)
            else:
                klist = list(ones.keys())
                kklist.insert(0, 'symbol')
                kklist.insert(1, 'ts')
                kklist.insert(2, 'tm_intv')
                kklist.insert(3, klist[4])
                kklist.insert(4, klist[0])
                kklist.insert(5, klist[1])
                kklist.insert(6, klist[6])
                kklist.insert(7, klist[2])
                kklist.insert(8, 'amount')
                kklist.insert(9, 'vol')
                kklist.insert(10, klist[5])
                w.writerow(kklist)

                additem2list(ts, vvlist, SYM, SOLUTION, ones)
                w.writerow(vvlist)

    # write original data to txt files
    with open(sTfilepath, 'a+', encoding='utf-8') as tf:
        tf.writelines(json.dumps(rdata) + '\n')


# add extral items to the original list
def additem2list(ts, vvlist, sym, ml, vitem):
    vvlist.insert(0, sym)
    vvlist.insert(1, ts)
    if ml == 'M1':  # when solution is M1, we will write 1m to csv
        ml = kline_interval
    vvlist.insert(2, ml)
    vvlist.insert(3, vitem['id'])
    vvlist.insert(4, vitem['open'])
    vvlist.insert(5, vitem['close'])
    vvlist.insert(6, vitem['low'])
    vvlist.insert(7, vitem['high'])
    vvlist.insert(8, vitem['quote_vol'])
    vvlist.insert(9, vitem['base_vol'])
    vvlist.insert(10, vitem['count'])


if __name__ == '__main__':
    print(sys.argv)
    SOLUTION = sys.argv[1]
    SYM = sys.argv[2]
    start_kline()

