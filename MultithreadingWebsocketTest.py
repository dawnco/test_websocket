#!/usr/bin/python
#-*- coding:utf-8 -*-
#__author__ == 'chenmingle'
#
#
# 结束任务  
# ps -ef | grep Multithread | grep -v grep | cut -c 9-15 | xargs kill -s 9

import random
import websocket
import time
import threading
import json
import multiprocessing
import signal
import os

from threadpool import ThreadPool, makeRequests





#修改成自己的websocket地址
WS_URL = "ws://192.168.0.11:9501/" 
#定义进程数
processes=10
#定义线程数（每个文件可能限制1024个，可以修改fs.file等参数）
thread_num=10

def on_message(ws, message):
     print(message)
     pass

def on_error(ws, error):
    print(error)
    pass

def on_close(ws):
    print("### closed ###")
    pass

def on_open(ws):
    def send_trhead():
        #设置你websocket的内容
        send_info = {"act": "refresh", "data": 'hello %s' % random.randint(1, 100)}
        #每隔10秒发送一下数据使链接不中断
        while True:
            time.sleep(10)
            ws.send(json.dumps(send_info))

    t = threading.Thread(target=send_trhead)
    t.start()

def on_start(num):
    time.sleep(num%20)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WS_URL + str(num),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

def thread_web_socket():
    #线程池
    pool = ThreadPool(thread_num)
    num = list()
    #设置开启线程的数量
    for ir in range(thread_num):
        num.append(ir)
    requests = makeRequests(on_start, num)
    [pool.putRequest(req) for req in requests]
    pool.wait()

if __name__ == "__main__":
    #进程池
    pool = multiprocessing.Pool(processes=processes)
    #设置开启进程的数量
    for i in xrange(processes):
        pool.apply_async(thread_web_socket)
    pool.close()
    pool.join()
