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
fcoin.auth('key ', 'secret')
sDir = os.path.join(os.path.abspath('..'), '..', 'Fcoin_DL')
stime = time.strftime('%Y', time.localtime())


def start_kline():
    while True:
        try:
            sync_kline()
        except Exception as error:
            print(error)
        time.sleep(2)


# 取K线数据
def sync_kline():
    for sy in config.sylist:
        # for original data
        sTfile = '{0}_{1}_{2}'.format(stime, sy, 'candle.txt')
        sTfilepath = os.path.join(sDir, 'KLineM1', sTfile)

        # save original data to csv
        sfile = '{0}_{1}_{2}'.format(stime, sy, 'candle.csv')
        sfilepath = os.path.join(sDir, 'KLineM1', sfile)
        rdata = fcoin.get_candle('M1', sy)
        candleinfo = rdata['data']  # M1 = 1分钟线，   取150条数据
        # print(candleinfo)
        sflag = 'open'
        rFind = False
        for ones in candleinfo:
            # print(ones)
            if os.path.exists(sfilepath):
                with open(sfilepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline()  # 取第一行
                    rFind = sflag in first_line
            with open(sfilepath, 'a+', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                if rFind is True:
                    vlist = list(ones.values())
                    w.writerow(vlist)
                else:
                    klist = list(ones.keys())
                    w.writerow(klist)
                    vlist = list(ones.values())
                    w.writerow(vlist)
            f.close()

            # write original data to txt files
            with open(sTfilepath, 'a+', encoding='utf-8') as tf:
                tf.writelines(json.dumps(rdata) + '\n')
                tf.close()


if __name__ == '__main__':
    start_kline()

