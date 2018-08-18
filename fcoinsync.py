# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging
import os
from config import kline_interval
from enums import Platform
from enums import Symbol
from fcoin import Fcoin
import csv
import time
import json

fcoin = Fcoin()
fcoin.auth('key ', 'secret')
datadir = os.path.join(os.path.abspath('..'), 'data')


class BaseSync(object):
    def __init__(self, platform, data_type):
        self.data_type = data_type
        self.platform = platform

    def run(self, *args):
        try:
            self.sync_data(*args)
        except Exception as error:
            print(error)

    # 取K线数据
    def sync_kline(self, *args):
        solution = args[0]
        sym = args[1]
        payload = args[2]
        sdir = args[3]
        stime = time.strftime('%Y%m%d', time.localtime())
        sdataDir = os.path.join(sdir, stime, solution)

        # print(sdataDir)
        if not os.path.exists(sdataDir):
            os.makedirs(sdataDir)

        sTfile = '{0}_{1}_{2}{3}'.format(self.data_type, stime, sym, '.txt')
        sTfilepath = os.path.join(sdataDir, sTfile)

        # save original data to csv
        sfile = '{0}_{1}_{2}{3}'.format(self.data_type, stime, sym, '.csv')
        sfilepath = os.path.join(sdataDir, sfile)
        rdata = fcoin.get_candle(solution, sym, **payload)  # 获取特定solution的kline数据
        candleinfo = rdata['data']

        sflag = 'open'
        rFind = False
        # print('单次获取的数据量：%s' % len(candleinfo))
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
                    self.additem2list(ticks, vvlist, sym, solution, ones)
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

                    self.additem2list(ts, vvlist, sym, solution, ones)
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

    # 日志初始化
    def _init_log(self):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')  # 格式

        '''
        保存文档
        '''
        handler = logging.FileHandler("appFcoin.log")
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self._log.addHandler(handler)

        '''
        控制台显示
        '''
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self._log.addHandler(console)