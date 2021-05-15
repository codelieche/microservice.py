# -*- coding:utf-8 -*-
import time
import threading

import grpc
from google.protobuf import empty_pb2

from proto.pb.stream_pb2 import NewsRequest, NewsResponse
from proto.pb.stream_pb2_grpc import NewsStoreStub


def test_news_store_get_news_ping(n=10):
    address = "0.0.0.0:9081"
    with grpc.insecure_channel(address) as channel:
        stub = NewsStoreStub(channel=channel)
        for i in range(n):
            r = empty_pb2.Empty()
            response = stub.Ping(r)
            print(i, "====>", response.message)
            print(response)
            time.sleep(i + 1 if i < 5 else 3)


def test_news_store_get_news_stream(n=10):
    address = "0.0.0.0:9081"
    with grpc.insecure_channel(address) as channel:
        stub = NewsStoreStub(channel=channel)

        # 获取消息
        request = NewsRequest(data="all")

        input_stream = stub.GetNewsStream(request)

        # 读取响应结果的函数
        def read_response():
            flag = True
            while flag:
                try:
                    item = next(input_stream)
                    print("received:{}".format(item.data))
                except StopIteration:
                    print("这次从服务器获取流结束了")
                    flag = False
                except Exception as e:
                    print("读取响应出错：", str(e))
                    flag = False

        thread = threading.Thread(target=read_response)
        thread.daemon = True
        thread.start()
        thread.join(timeout=100)


def test_news_store_put_news_stream(n=10):
    address = "0.0.0.0:9081"
    with grpc.insecure_channel(address) as channel:
        stub = NewsStoreStub(channel=channel)

        def generate_news(n):
            for i in range(n):
                time.sleep(1)
                data = "i am news {}".format(i+1)
                news = NewsResponse(data=data)
                yield news

        put_stream = generate_news(n)

        response = stub.PutNewsStream(put_stream)
        print('put done:', response)


def test_news_store_get_put_news_stream(n=10):
    address = "0.0.0.0:9081"
    with grpc.insecure_channel(address) as channel:
        stub = NewsStoreStub(channel=channel)

        # 发送消息的函数
        def stream():
            flag = True
            while flag:
                data = input('$ ')
                yield NewsRequest(data=data)
                if data == 'close':
                    flag = False

        input_stream = stub.GetPutNewsStream(stream())

        # 读取响应结果的函数
        def read_response():
            while True:
                item = next(input_stream)
                print("received:{}".format(item.data))

        thread = threading.Thread(target=read_response)
        thread.daemon = True
        thread.start()

        while True:
            time.sleep(1)


if __name__ == "__main__":
    test_news_store_get_news_ping()

    # test_news_store_get_news_stream()

    # test_news_store_put_news_stream()

    # test_news_store_get_put_news_stream()
