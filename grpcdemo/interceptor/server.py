# -*- coding:utf-8 -*-
import datetime

import grpc


class RequestInfoPrint(grpc.ServerInterceptor):
    """
    打印请求信息拦截器
    注意在golang中是函数，python中是继承基类，然后实现某几个方法
    """

    def __init__(self):
        print('服务端拦截器初始化:', RequestInfoPrint)

    def intercept_service(self, continuation, handler_call_details):
        # 1. 开始处理请求前相关操作
        # 1-1: 记录消息
        start = datetime.datetime.now()
        msg = f"请求: {handler_call_details.method}"
        print(msg)
        # 1-2：打印metadata
        print("\t请求metadata:")
        for item in handler_call_details.invocation_metadata:
            print(f"\t{item.key}:\t{item.value}")

        # 2. 处理请求
        response = continuation(handler_call_details)

        # 3. 处理完请求之后的操作

        print("{} 耗时: {}\n".format(msg, datetime.datetime.now() - start))
        return response

