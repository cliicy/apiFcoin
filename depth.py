# # -*- coding: utf-8 -*-
"""

"""

from fcoin import Fcoin
import os,csv,time


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
    sylist = ['btcusdt','ethusdt','bchusdt','ltcusdt','ftusdt','fteth','etcusdt','ftbtc','bnbusdt','btmusdt','zrxeth']
    sDir = os.path.join(os.path.abspath('..'),'..','Fcoin_DL')
    stime = time.strftime('%Y',time.localtime())

    # 获取最新的深度明细
    # 买(卖)1价, 买(卖)1量
    bids_head = ['买1价','买的量数']
    bids_flag = '买1价'
    asks_head = ['卖1价','卖的量数']
    asks_flag = '卖1价'
    for sy in sylist:
        bidsfile = '{0}_{1}_{2}'.format(stime,sy, 'bids.csv')
        bidspath = os.path.join(sDir,'depth', bidsfile)

        asksfile = '{0}_{1}_{2}'.format(stime, sy, 'asks.csv')
        askspath = os.path.join(sDir,'depth', asksfile)

        depthinfo = fcoin.get_market_depth('L20',sy)['data']# 20 档行情深度 for iask in depthinfo['asks']:
        bidlists = depthinfo['bids']
        print(bidlists)
        asklists = depthinfo['asks']
        print(asklists)
        nask = len(depthinfo['asks'])
        nbid = len(depthinfo['bids'])
        iask = 0
        rFindasks = False
        while iask < nask:
            if os.path.exists(askspath):
                with open(askspath, 'r', encoding='utf-8') as f:
                    first_line = f.readline()  # 取第一行
                    rFindasks = asks_flag in first_line
            with open(askspath, 'a+', encoding='utf-8',newline='') as f:
                w = csv.writer(f)
                if rFindasks is True:
                    w.writerow(asklists[iask:iask + 2])
                    iask += 2

                else:
                    w.writerow(asks_head)
                    w.writerow(asklists[iask:iask+2])
                    iask += 2
        f.close()

        ibid = 0
        rFindbids = False
        while ibid < nbid:
            if os.path.exists(bidspath):
                with open(bidspath, 'r', encoding='utf-8') as f:
                    first_line = f.readline()  # 取第一行
                    rFindbids = bids_flag in first_line
            with open(bidspath, 'a+', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                if rFindbids is True:
                    w.writerow(bidlists[ibid:ibid + 2])
                    ibid += 2
                else:
                    w.writerow(bids_head)
                    w.writerow(bidlists[ibid:ibid + 2])
                    ibid += 2
        f.close()

if __name__ == '__main__':
    start_depth()