# -*- coding:utf-8 -*-
import datetime
import grpc


class RequestBeforePrint(grpc.UnaryUnaryClientInterceptor):
    """
    打印请求信息拦截器
    注意在golang中是函数，python中是继承基类，然后实现某几个方法
    """

    def intercept_unary_unary(self, continuation, client_call_details, request):
        # 1. 向grpc服务端发起请求之前操作
        start = datetime.datetime.now()
        msg = f"请求：{client_call_details.method}"
        # print(msg)

        # 2. 向服务端发起请求
        response = continuation(client_call_details, request)

        # 3. 请求发送完毕后相关操作
        print(f"\t{msg} 耗时:", datetime.datetime.now() - start)
        return response
