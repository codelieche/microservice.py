# -*- coding:utf-8 -*-
import time

import grpc

from proto.pb.hello_pb2_grpc import GreeterStub
from proto.pb.hello_pb2 import HelloRequest


def test_hello_greeter_sayhello(n=10):
    address = "0.0.0.0:9081"
    with grpc.insecure_channel(address) as channel:
        stub = GreeterStub(channel=channel)
        for i in range(n):
            request = HelloRequest(content=f"Hello Test: {i + 1}")

            response = stub.SayHello(request)
            print(response.message)
            print(response)
            time.sleep(i + 1 if i < 5 else 3)


if __name__ == "__main__":
    test_hello_greeter_sayhello()
