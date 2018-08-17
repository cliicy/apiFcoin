# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging
import time


class BaseSync(object):
    def __init__(self, platform, data_type):
        self.data_type = data_type
        self.platform = platform

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

    def run(self, *args):
        try:
            self.sync_kline(*args)
        except Exception as error:
            print(error)
