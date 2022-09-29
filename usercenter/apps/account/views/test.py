# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated


class TestView(APIView):
    """
    测试api
    """
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        meta = request.META
        content = {
            "status": True,
            "ip": meta["REMOTE_ADDR"],
            "agent": meta["HTTP_USER_AGENT"],
        }
        return Response(content)
