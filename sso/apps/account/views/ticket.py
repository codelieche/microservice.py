# -*- coding:utf-8 -*-
import datetime

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.http.response import JsonResponse

from account.models.ticket import Ticket
from account.serializers.ticket import TicketModelSerializer, TicketInfoSerializer


class TicketListApiView(generics.ListAPIView):
    """
    登录券列表api
    """
    serializer_class = TicketModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.filter(user=user)
        return queryset


class TicketDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    登录券详情api
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketModelSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    def get_object(self):
        instance = super().get_object()
        user = self.request.user
        if user.is_superuser:
            return instance
        else:
            if instance.user == user:
                return instance
            else:
                return None


class TicketCheckApiView(APIView):
    """
    登录券校验
    """

    def get(self, request):
        # 第1步：获取ticket
        # 1-1：获取ticket name
        ticket_name = request.GET.get("ticket")

        # 1-2：检查ticket name
        if not ticket_name:
            content = {
                "status": False,
                "message": "请传入ticket"
            }
            return JsonResponse(data=content, status=400)

        # 1-3：获取ticket
        ticket = Ticket.objects.filter(name=ticket_name).first()
        if not ticket:
            content = {
                "status": False,
                "message": "传入的ticket({})不存在".format(ticket_name)
            }
            return JsonResponse(data=content, status=400)

        # 1-4: 判断ticket是否被使用了
        if not ticket.is_active:
            content = {
                "status": False,
                "message": "传入的ticket({})已不可使用".format(ticket_name)
            }
            return JsonResponse(data=content, status=400)

        # 1-5: 判断ticket是否过期
        sub_time = ticket.time_expired - datetime.datetime.now()
        if sub_time.total_seconds() < 0:
            ticket.is_active = False
            ticket.save()
            content = {
                "status": False,
                "message": "传入的ticket({})已经过期".format(ticket_name)
            }
            return JsonResponse(data=content, status=400)

        # 第2步：校验return_url:(暂时不校验returnUrl，让其它系统中间件自行判断)
        # return_url = request.GET.get("returnUrl")
        # if return_url != ticket.return_url:
        #     content = {
        #         "status": False,
        #         "message": "传入的ticket不可用于跳转这个地址({})".format(return_url)
        #     }
        #     return JsonResponse(data=content, status=400)

        # 第3步：修改ticket的信息
        ticket.is_active = False
        ticket.save()

        # 第4步：返回用户信息和sessionid
        serializer = TicketInfoSerializer(ticket)
        content = {
            "status": True,
            "message": "ticket有效",
            "data": serializer.data,
        }
        return JsonResponse(data=content, status=200)



