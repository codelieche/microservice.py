# -*- coding:utf-8 -*-
"""
网站首页
"""
from django.shortcuts import render


def index_page(request):
    # 网站首页
    # print(request.META["REMOTE_ADDR"])
    address = ""
    try:
        if 'REMOTE_ADDR' in request.META:
            address = request.META["REMOTE_ADDR"]
    except Exception as e:
        print(str(e))

    data = {
        "title": "Index",
        "system": "Demo",
        "content": "你好！{}".format(address)
    }
    return render(request, 'index.html', data)
