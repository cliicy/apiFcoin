# -*- coding: utf-8 -*-
"""
M1 获取最多的数据条数： 2000 是按照距离运行时间为止的前2000条  或者1440条数据
可以再解析这2000/1440+条数据
M1 = 1分钟线，   取150条数据
D1 = 1天线，   取102天的数据
"""
from enums import Platform
from enums import PlatformDataType
import os
import sys
from fcoinsync import BaseSync
from fcoinsync import datadir
import time
from config import time_spot


class SyncCandle(BaseSync):
    def __init__(self):
        self.solution = ''
        self.sym = ''
        self.platform = Platform.PLATFORM_FCOIN.value
        self.data_type = PlatformDataType.PLATFORM_DATA_KLINE.value
        self.bsync = BaseSync(self.platform, self.data_type)

    def sync_kline(self, *args):
        self.solution = args[0]
        payload = {'limit': 1440}
        sdir = os.path.join(datadir, 'rest_http', 'M1All_kline')
        aparam = (args[0], args[1], payload, sdir)
        self.bsync.sync_kline(*aparam)

    def run(self, *args):
        while True:
            st = time.strftime('%H:%M:%S', time.localtime())
            if st == time_spot:
                print('开始获取1440条数据kline数据：一天获取一次')
                self.sync_kline(*args)
                time.sleep(86400)  # 24*60*60
            time.sleep(0.1)


if __name__ == '__main__':
    print(sys.argv)
    SOLUTION = sys.argv[1]
    SYM = sys.argv[2]

