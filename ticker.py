# # -*- coding: utf-8 -*-
"""

"""

from fcoin import Fcoin
import os
import csv
import time
import json
import config

fcoin = Fcoin()
sDir = os.path.join(os.path.abspath('..'), '..', 'Fcoin_DL')
stime = time.strftime('%Y', time.localtime())

print("获取交易的Ticks: ")
headl = [
  "最新成交价",
  "最近一笔成交的成交量",
  "最大买一价",
  "最大买一量",
  "最小卖一价",
  "最小卖一量",
  "24小时前成交价",
  "24小时内最高价",
  "24小时内最低价",
  "24小时内基准货币成交量",# , 如 btcusdt 中 btc 的量
  "24小时内计价货币成交量"] #, 如 btcusdt 中 usdt 的量


def start_ticker():
    while True:
        try:
            sync_ticker()
        except Exception as err:
            print(err)
        time.sleep(2)


def sync_ticker():
    sflag = '最新成交价'
    rFind = False
    for item in config.sylist:
        # for original data
        sTfile = '{0}_{1}_{2}'.format(stime, item, 'ticker.txt')
        sTfilepath = os.path.join(sDir, 'ticker', sTfile)

        rdata = fcoin.get_market_ticker(item)
        tdata = rdata['data']['ticker']

        # save return data to csv files
        sfile = '{0}_{1}{2}'.format(item, stime, '.csv')
        sfilepath = os.path.join(sDir, 'ticker', sfile)
        if os.path.exists(sfilepath):
            with open(sfilepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFind = sflag in first_line
        with open(sfilepath, 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            if rFind is True:
                w.writerow(tdata)
            else:
                w.writerow(headl)
                w.writerow(tdata)
        f.close()
        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(rdata) + '\n')
            tf.close()


if __name__ == '__main__':
    start_ticker()
