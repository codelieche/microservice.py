# -*- coding:utf-8 -*-
import string
import time
import threading
import random
from concurrent import futures

import grpc

from proto.pb.stream_pb2_grpc import NewsStoreServicer, add_NewsStoreServicer_to_server
from proto.pb.stream_pb2 import NewsRequest, NewsResponse


class NewsStoreService(NewsStoreServicer):

    def __int__(self):
        print("初始化")
        super().__init__()

    def GetNewsStream(self, request, context):
        print("收到请求：", request.data, context)

        for i in range(10):
            time.sleep(i+1 if i > 5 else 3)
            yield NewsResponse(data="News {} data".format(i+1))

    def PutNewsStream(self, request_iterator, context):
        for item in request_iterator:
            print("item:", item)

        return NewsResponse(data="123456")

    def GetPutNewsStream(self, request_iterator, context):
        def output():
            while True:
                time.sleep(1)
                yield random.choice(string.ascii_letters)

        output_stream = output()

        def read_input():
            flag = True
            while flag:
                try:
                    received = next(request_iterator)
                    print('received:{}'.format(received))
                    if received.data == "close":
                        print("读取应该关闭了，不会再发送消息")
                        flag = False
                except StopIteration:
                    flag = False
                except Exception as e:
                    print("读取消息出现错误：", str(e))
                    flag = False

        thread = threading.Thread(target=read_input)
        thread.daemon = True
        thread.start()

        while True:
            # time.sleep(1)
            yield NewsResponse(data=next(output_stream))


def run_news_store_server(address="0.0.0.0:9081"):
    # 1. 实例化grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 2. 注册逻辑到server中
    add_NewsStoreServicer_to_server(servicer=NewsStoreService(), server=server)

    # 3. 启动server
    # 开发测试使用insecure_port
    server.add_insecure_port(address=address)
    server.start()
    # wait
    server.wait_for_termination()


if __name__ == "__main__":
    run_news_store_server()
