# -*- coding:utf-8 -*-
import time
import unittest

import grpc

from google.protobuf import empty_pb2

# from proto.pb.base_pb2 import Pong
from proto.pb.hello_pb2_grpc import GreeterStub
from proto.pb.hello_pb2 import HelloRequest

from interceptor.client import RequestBeforePrint


def test_hello_greeter_ping(n=10):
    address = "0.0.0.0:9081"
    with grpc.insecure_channel(address) as channel:
        stub = GreeterStub(channel=channel)
        for i in range(n):
            r = empty_pb2.Empty()
            response = stub.Ping(r)
            print(i, "====>", response.message)
            print(response)
            time.sleep(i + 1 if i < 5 else 3)


def test_hello_greeter_sayhello(n=10):
    address = "0.0.0.0:9081"
    with grpc.insecure_channel(address) as channel:
        stub = GreeterStub(channel=channel)
        for i in range(n):
            request = HelloRequest(message=f"Hello Test: {i + 1}")

            response = stub.SayHello(request)
            print(response.message)
            print(response)
            time.sleep(i + 1 if i < 5 else 3)


class GreeterServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        print("setup:", self._testMethodName)
        self.address = "127.0.0.1:9081"
        # 获取grpc client
        if self._testMethodName.endswith("with_interceptor"):
            self.connect_stub_with_interceptor()
        else:
            self.connect_stub()

        # 相关配置
        self.request_times = 2

        # 公共的请求数据
        self.ping_request = empty_pb2.Empty()

    def connect_stub(self):
        self.channel = grpc.insecure_channel(self.address)
        self.stub = GreeterStub(self.channel)

    def connect_stub_with_interceptor(self):
        channel = grpc.insecure_channel(self.address)
        default_interceptor = RequestBeforePrint()
        self.channel = grpc.intercept_channel(channel, default_interceptor)

        self.stub = GreeterStub(self.channel)

    def test_ping(self):
        print('test_ping start')
        for i in range(self.request_times):
            response = self.stub.Ping(self.ping_request)
            print("\t{} ====>: status: {}, message: {}".format(i, response.status, response.message))
            self.assertEqual(response.status, True, "ping error")
            time.sleep(1)
        print('test_ping end')

    def test_ping_with_metadata(self):
        print('test_ping_with_metadata start')

        for i in range(self.request_times):
            response, call = self.stub.Ping.with_call(
                self.ping_request,
                metadata=(
                    ('user', 'root'),
                    ('password', 'password value'),
                    ('token', 'token value'),
                )
            )
            print("\t{} ====>: status: {}, message: {}".format(i, response.status, response.message))
            self.assertEqual(response.status, True, "ping error")
            time.sleep(1)

        # 答应出call的信息
        if call.trailing_metadata():
            print('\tcall.trailing_metadata(): ', call.trailing_metadata())
            for key, value in call.trailing_metadata():
                print('\t received trailing metadata: {} :\t {}'.format(key, value))
        print('test_ping_with_metadata end')

    def test_ping_with_interceptor(self):
        print('test_ping_with_interceptor start')

        for i in range(self.request_times):
            response, call = self.stub.Ping.with_call(
                self.ping_request,
                metadata=(
                    ('user', 'root_interceptor'),
                    ('password', 'password_value'),
                    ('token', 'token_value'),
                )
            )
            print("\t{} ====>: status: {}, message: {}".format(i, response.status, response.message))
            self.assertEqual(response.status, True, "ping error")
            time.sleep(1)

        # 答应出call的信息
        if call.trailing_metadata():
            print('\tcall.trailing_metadata(): ', call.trailing_metadata())
            for key, value in call.trailing_metadata():
                print('\t received trailing metadata: {} :\t {}'.format(key, value))
        print('test_ping_with_interceptor end')

    def tearDown(self) -> None:
        print('tearDown: {}\n'.format(self._testMethodName))
        self.channel.close()


if __name__ == "__main__":
    print("start test suite")
    # 1. 实例化 test suite
    suite = unittest.TestSuite()

    # 2. 添加想要的测试函数
    # suite.addTest(GreeterServiceTest('test_ping'))
    # suite.addTest(GreeterServiceTest('test_ping_with_metadata'))
    suite.addTest(GreeterServiceTest('test_ping_with_interceptor'))

    print("suite.countTestCases():", suite.countTestCases())

    # 3. 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)

    print("Done")

    # test_hello_greeter_ping()

    # test_hello_greeter_sayhello()
