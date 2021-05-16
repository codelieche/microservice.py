# -*- coding:utf-8 -*-
import datetime

import grpc

from concurrent import futures

from proto.pb.base_pb2 import Pong
from proto.pb.hello_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from proto.pb.hello_pb2 import HelloResponse

from interceptor.server import RequestInfoPrint


class HelloGreeter(GreeterServicer):

    def Ping(self, request, context):
        print(datetime.datetime.now().strftime("%F %T"), "收到ping请求")
        pong = Pong(status=True, message="Pong")
        return pong

    def SayHello(self, request, context):
        print(datetime.datetime.now().strftime("%F %T"), "收到请求：", request)
        msg = f"request: -->: {request.message}, response!"
        response = HelloResponse(message=msg)
        return response


def run_greeter_server(address="0.0.0.0:9081"):
    # 1. 实例化grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 2. 注册逻辑到server中
    add_GreeterServicer_to_server(servicer=HelloGreeter(), server=server)

    # 3. 启动server
    # 开发测试使用insecure_port
    server.add_insecure_port(address=address)
    server.start()
    # wait
    server.wait_for_termination()


def run_greeter_server_with_interceptor(address="0.0.0.0:9081"):
    # 1. 实例化grpc server
    interceptor_01 = RequestInfoPrint()
    interceptors = (interceptor_01,)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)

    # 2. 注册逻辑到server中
    add_GreeterServicer_to_server(servicer=HelloGreeter(), server=server)

    # 3. 启动server
    # 开发测试使用insecure_port
    server.add_insecure_port(address=address)
    server.start()
    # wait
    server.wait_for_termination()


if __name__ == "__main__":
    addr = "0.0.0.0:9081"
    # start server
    # run_greeter_server(address=addr)
    run_greeter_server_with_interceptor(address=addr)
