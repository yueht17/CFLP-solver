#! usr/bin/env python
# -*- coding:utf-8 -*-

def logPrint(func):
    import time
    # 定义嵌套函数，用来打印出装饰的函数的执行时间

    def wrapper(*args, **kwargs):
        # 定义开始时间
        tic = time.time()
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("[INFO]|{}|{:15}|{}".format(start_time, func.__name__, "begin"))
        tic = time.time()
        func_return = func(*args, **kwargs)
        toc = time.time()
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("[INFO]|{}|{:15}|{}|TimeSpend:{:.2f}s".format(end_time, func.__name__, "finish", toc - tic))

        return func_return

    return wrapper
