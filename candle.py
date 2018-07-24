# # -*- coding: utf-8 -*-
"""

"""


from fcoin import Fcoin
import os,csv,time
import requests

fcoin = Fcoin()
fcoin.auth('key ', 'secret')
sylist = ['btcusdt','ethusdt','bchusdt','ltcusdt','ftusdt','fteth','etcusdt','ftbtc','bnbusdt','btmusdt','zrxeth']
sDir = os.path.join(os.path.abspath('..'),'..','Fcoin_DL')
stime = time.strftime('%Y',time.localtime())


# 取K线数据
def sync_Kline():
    for sy in sylist:
        sfile = '{0}_{1}_{2}'.format(stime, sy, 'candle.csv')
        sfilepath = os.path.join(sDir,'KLine', sfile)
        candleinfo = fcoin.get_candle('M1', sy)['data']  # M1 = 1分钟线，   取150条数据
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


if __name__ == '__main__':
    try:
        while True:
            sync_Kline()
    except Exception as err:
        print(err)
        time.sleep(5)
        sync_Kline()

