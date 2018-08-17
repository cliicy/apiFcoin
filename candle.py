# -*- coding: utf-8 -*-
"""
M1 获取最多的数据条数： 2000 是按照距离运行时间为止的前2000条  或者1440条数据
可以再解析这2000/1440+条数据
M1 = 1分钟线，   取150条数据
D1 = 1天线，   取102天的数据
"""
from fcoin import Fcoin
from config import kline_interval
from enums import Symbol
from enums import Platform
from enums import PlatformDataType
import os
import csv
import time
import json
import sys
from fcoinsync import BaseSync

sDir = os.path.abspath(os.path.join(os.path.abspath('..'), 'data', 'rest_http', 'M1All_kline'))
stime = time.strftime('%Y%m%d', time.localtime())
fcoin = Fcoin()
fcoin.auth('key ', 'secret')


class SyncCandle(BaseSync):
    def __init__(self):
        self.solution = ''
        self.sym = ''
        self.platform = Platform.PLATFORM_FCOIN.value
        self.data_type = PlatformDataType.PLATFORM_DATA_KLINE.value
        BaseSync(self.platform, self.data_type)

    # 取K线数据
    def sync_kline(self, *args):
        self.solution = args[0]
        self.sym = args[1]
        sdataDir = os.path.join(sDir, stime, self.solution)
        # print(sdataDir)
        if not os.path.exists(sdataDir):
            os.makedirs(sdataDir)

        sTfile = '{0}_{1}_{2}{3}'.format(self.data_type, stime, self.sym, '.txt')
        sTfilepath = os.path.join(sdataDir, sTfile)

        # save original data to csv
        sfile = '{0}_{1}_{2}{3}'.format(self.data_type, stime, self.sym, '.csv')
        sfilepath = os.path.join(sdataDir, sfile)

        # rdata = fcoin.get_candlem1All(SOLUTION, SYM)  # 获取特定solution的kline数据
        payload = {'limit': 1442}
        rdata = fcoin.get_candle(self.solution, self.sym, **payload)  # 获取特定solution的kline数据
        candleinfo = rdata['data']

        sflag = 'open'
        rFind = False
        print('单次获取的数据量：%s' % len(candleinfo))
        for ones in candleinfo:
            # print(ones)
            # 从服务器得到的数据中没有ts，只有id，根据文档要求，要把获取到数据的时间存入csv文件及数据库中
            ts = int(round(ones['id'] * 1000))
            ticks = ts  # int(round(time.time() * 1000))
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
                    self.additem2list(ticks, vvlist, self.sym, self.solution, ones)
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

                    self.additem2list(ts, vvlist, self.sym, self.solution, ones)
                    w.writerow(vvlist)

        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(rdata) + '\n')

    # add extral items to the original list
    @staticmethod
    def additem2list(ts, vvlist, sym, ml, vitem):
        sym = Symbol.convert_to_standard_symbol(Platform.PLATFORM_FCOIN, sym)
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

