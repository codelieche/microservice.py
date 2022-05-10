# -*- coding:utf-8 -*-
import grpc

from concurrent import futures

from proto.pb.hello_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from proto.pb.hello_pb2 import HelloResponse


class HelloGreeter(GreeterServicer):
    def SayHello(self, request, context):
        msg = f"request: -->: {request.content}, response!"
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


if __name__ == "__main__":
    addr = "0.0.0.0:9081"
    run_greeter_server(address=addr)