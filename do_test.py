#!/usr/bin/env python

import threading
import time


class Test(threading.Thread):
    def __init__(self):
        pass

    def test(self):
        print('run test!')

    def run(self):
        while True:
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
            self.test()
            time.sleep(5)


# test...
a = Test()
a.run()


# import threading
# import time
#
#
# class MyThread(threading.Thread):
#
#     def __init__(self, func, args, name=''):
#         threading.Thread.__init__(self)
#         self.name=name
#         self.func=func
#         self.args=args
#
#     def run(self):
#         apply(self.func, self.args)
#         print('run run')
#
#
# def print_func(num):
#
#     while True:
#         print("I am thread%d" % num)
#         time.sleep(1)
#
#
# threads = []
# t1 = MyThread(print_func, (1, ), print_func.__name__)
# threads.append(t1)
# t2 = MyThread(print_func, (2, ), print_func.__name__)
# threads.append(t2)
#
#
# for t in threads:
#     t.setDaemon(True)
#     t.start()
#
# print("ok\n")
