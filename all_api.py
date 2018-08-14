# # -*- coding: utf-8 -*-
"""

"""


import pandas as pd 
from fcoin import Fcoin
import os,csv,time

fcoin = Fcoin()
fcoin.auth('key ', 'secret')
sylist = ['btcusdt','ethusdt','bchusdt','ltcusdt','ftusdt','fteth','etcusdt','ftbtc','bnbusdt','btmusdt','zrxeth']
sDir = os.path.join(os.path.abspath('..'),'..','Fcoin_DL','KLine')
stime = time.strftime('%Y-%m-%d',time.localtime())

# 获取最新的深度明细
# 买(卖)1价, 买(卖)1量
# The ask price is what sellers are willing to take for it.
# If you are selling a stock, you are going to get the bid price,
# if you are buying a stock you are going to get the ask price.
bids_head = ['买1价','买的量数']
bids_flag = '买1价'
asks_head = ['卖1价','卖的量数']
asks_flag = '卖1价'
for sy in sylist:
    bidsfile = '{0}_{1}_{2}'.format(stime,sy, 'bids_depth.csv')
    bidspath = os.path.join(sDir, bidsfile)

    asksfile = '{0}_{1}_{2}'.format(stime, sy, 'asks_depth.csv')
    askspath = os.path.join(sDir, asksfile)

    depthinfo = fcoin.get_market_depth('L20',sy)['data']# 20 档行情深度 for iask in depthinfo['asks']:
    bidlists = depthinfo['bids']
    print(bidlists)
    asklists = depthinfo['asks']
    print(asklists)
    nask = len(depthinfo['asks'])
    nbid = len(depthinfo['bids'])
    iask = 0
    rFindasks = False
    while iask < nask/2:
        if os.path.exists(askspath):
            with open(askspath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFindasks = asks_flag in first_line
        with open(askspath, 'a+', encoding='utf-8',newline='') as f:
            w = csv.writer(f)
            if rFindasks is True:
                print(asklists[iask])
                w.writerow(str(asklists[iask]))
                print(asklists[iask+1])
                w.writerow(str(asklists[iask+1]))
                iask += 2
            else:
                w.writerow(asks_head)
                ss = asklists[iask]
                print(ss)
                w.writerow(ss)
                ss = asklists[iask+1]
                w.writerow(ss)
                iask += 2
    f.close()

    ibid = 0
    rFindbids = False
    while ibid < nbid/2:
        if os.path.exists(bidspath):
            with open(bidspath, 'r', encoding='utf-8') as f:
                first_line = f.readline()  # 取第一行
                rFindbids = bids_flag in first_line
        with open(bidspath, 'a+', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            if rFindbids is True:
                w.writerow(bidlists[ibid])
                w.writerow(bidlists[ibid+1])
                ibid += 2
            else:
                w.writerow(bids_flag)
                w.writerow(str(bidlists[ibid]))
                w.writerow(str(bidlists[ibid+1]))
                ibid += 2
    f.close()

    # sflag = 'open'
    # rFind = False
    # for ones in depthinfo:
    #     print(ones)
    #     if os.path.exists(sfilepath):
    #         with open(sfilepath, 'r', encoding='utf-8') as f:
    #             first_line = f.readline()  # 取第一行
    #             rFind = sflag in first_line
    #     with open(sfilepath, 'a+', encoding='utf-8', newline='') as f:
    #         w = csv.writer(f)
    #         if rFind is True:
    #             vlist = list(ones.values())
    #             w.writerow(vlist)
    #         else:
    #             klist = list(ones.keys())
    #             w.writerow(klist)
    #             vlist = list(ones.values())
    #             w.writerow(vlist)
    #     f.close()

print('ooo')
exit(0)


# 取K线数据
for sy in sylist:
    sfile = '{0}_{1}_{2}'.format(stime,sy, 'candle.csv')
    sfilepath = os.path.join(sDir, sfile)
    candleinfo = fcoin.get_candle('M1', sy)['data']# M1 = 1分钟线，   取150条数据
    print(candleinfo)
    sflag = 'open'
    rFind = False
    for ones in candleinfo:
        print(ones)
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

print('ooo')
exit(0)

# 取得当前账户信息
print("取得当前账户信息: ")
acinfo =  fcoin.get_balance()
print(acinfo)
sfile = '{0}_{1}'.format(stime, 'acbalance.csv')
sfilepath = os.path.join(sDir,sfile)
dataframe = pd.DataFrame(acinfo,index=[0])
dataframe.to_csv(sfilepath,index=False,sep=',')
exit(0)
# symbol 表示对应交易币种. 所有币种区分的 topic 都在 topic 末尾
print('取得symbol: ')
syminfo = fcoin.get_symbols()
rFind = False
sfile = '{0}_{1}'.format(stime, 'allsyminfo.csv')
sfilepath = os.path.join(sDir,sfile)
sflag = 'amount_decimal'
for ones in syminfo:
    print(ones)
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

sflag = '最新成交价'
# sDir = os.path.join(os.path.abspath('..'),'..','Fcoin_DL','KLine')
rFind = False
for item in sylist:
    tdata = fcoin.get_market_ticker(item)['data']['ticker']
    # print(tdata)
    sfile = '{0}_{1}{2}'.format(item, stime, '.csv')
    sfilepath = os.path.join(sDir,sfile)
    if os.path.exists(sfilepath):
        with open(sfilepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()  # 取第一行
            rFind = sflag in first_line
    with open(sfilepath, 'a+', encoding='utf-8',newline='') as f:
        w = csv.writer(f)
        if rFind is True:
            w.writerow(tdata)
        else:
            w.writerow(headl)
            w.writerow(tdata)
    f.close()

# print("取得可交易的数字货币总类: ")
# allvbill = fcoin.get_currencies()

#
#print(fcoin.buy('fteth', 0.0001, 10))
#

