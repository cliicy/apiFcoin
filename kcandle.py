# # -*- coding: utf-8 -*-
"""

"""
import os
import time
import sys
from enums import Platform
from enums import PlatformDataType
from fcoinsync import BaseSync
from fcoinsync import datadir
from config import time_spot


class SyncMDCandle(BaseSync):
    def __init__(self):
        self.solution = ''
        self.platform = Platform.PLATFORM_FCOIN.value
        self.data_type = PlatformDataType.PLATFORM_DATA_KLINE.value
        self.bsync = BaseSync(self.platform, self.data_type)

    def run(self, *args):
        while True:
            st = time.strftime('%H:%M:%S', time.localtime())
            if st == time_spot:
                print('开始获取kline数据：')
                self.sync_kline(*args)
                if self.solution == 'M1':  # 1分 默认获得150条数据
                    time.sleep(9000)  # 150*60 = 9000
                elif self.solution == 'D1':  # 1天 默认传回102条数据
                    time.sleep(6120)  # 102*60
            time.sleep(0.1)

    # 取K线数据
    def sync_kline(self, *args):
        self.solution = args[0]
        payload = {}
        sdir = os.path.join(datadir, 'rest_http', 'kline')
        aparam = (args[0], args[1], payload, sdir)
        self.bsync.sync_kline(*aparam)


if __name__ == '__main__':
    print(sys.argv)
    SOLUTION = sys.argv[1]
    SYM = sys.argv[2]

