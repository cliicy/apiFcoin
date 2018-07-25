# # -*- coding: utf-8 -*-
"""

"""

from fcoin import Fcoin
import os
import csv
import time
import config
import json


def start_depth():
    while True:
        try:
            sync_depth()
        except Exception as err:
            print(err)
    time.sleep(2)


def sync_depth():
    fcoin = Fcoin()
    # fcoin.auth('key ', 'secret')
    sDir = os.path.join(os.path.abspath('..'), '..', 'Fcoin_DL')
    stime = time.strftime('%Y', time.localtime())
    rootn = 'depth'
    level = 'L20'
    dirname = '{0}{1}'.format(rootn,level)
    # 获取最新的深度明细
    # 买(卖)1价, 买(卖)1量
    depth_head = ['买1价', '买的量数', '卖1价', '卖的量数']
    depth_flag = '买1价'
    # asks_head = ['卖1价','卖的量数']
    # asks_flag = '卖1价'
    for sy in config.sylist:
        # for original data
        sTfile = '{0}_{1}_{2}'.format(stime, sy, '{0}{1}'.format(rootn, '.txt'))
        sTfilepath = os.path.join(sDir, dirname, sTfile)

        dpfile = '{0}_{1}_{2}'.format(stime, sy, '{0}{1}'.format(rootn, '.csv'))
        dpspath = os.path.join(sDir, dirname, dpfile)

        rdata = fcoin.get_market_depth(level, sy)
        depthinfo = rdata['data']# 20 档行情深度 for iask in depthinfo['asks']:
        bidlists = depthinfo['bids']
        print(bidlists)
        asklists = depthinfo['asks']
        print(asklists)
        idp = 0

        nask = len(depthinfo['asks'])
        # nbid = len(depthinfo['bids'])
        rFind = False
        while idp < nask:
            if os.path.exists(dpspath):
                with open(dpspath, 'r', encoding='utf-8') as f:
                    first_line = f.readline()  # 取第一行
                    rFind = depth_flag in first_line
            with open(dpspath, 'a+', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                balist = []
                # balist = list(bidlists[idp:idp + 2] )
                balist.extend(bidlists[idp:idp + 2])
                balist.extend(asklists[idp:idp + 2])
                if rFind is True:
                    w.writerow(balist)
                    idp += 2

                else:
                    w.writerow(depth_head)
                    w.writerow(balist)
                    idp += 2
        f.close()

        # write original data to txt files
        with open(sTfilepath, 'a+', encoding='utf-8') as tf:
            tf.writelines(json.dumps(rdata) + '\n')
            tf.close()


if __name__ == '__main__':
    start_depth()