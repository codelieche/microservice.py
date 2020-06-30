# -*- coding:utf-8 -*-
"""
安全日志的视图
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from account.models.safelog import SafeLog
from account.serializers.safelog import SafeLogModelSerializer


class SafeLogListApiView(generics.ListAPIView):
    """
    安全日志列表页api
    """
    serializer_class = SafeLogModelSerializer
    queryset = SafeLog.objects.all()
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("user__username", "content")
    filter_fields = ("user", "category", "success")
    ordering = ("id", "success", "category", "time_added")
    ordering = ("-id",)

    def get_queryset(self):
        # 1. 判断是否是超级用户
        user = self.request.user
        if user.is_superuser:
            queryset = SafeLog.objects.all().order_by("-id")
        else:
            queryset = SafeLog.objects.filter(user=user).order_by("-id")

        # 2. 对日期进行过滤
        date_added__gte = self.request.query_params.get("date_added__gte")
        date_added__lte = self.request.query_params.get("date_added__lte")
        if date_added__gte:
            queryset = queryset.filter(time_added__date__gte=date_added__gte)
        if date_added__lte:
            queryset = queryset.filter(time_added__date__lte=date_added__lte)
        return queryset
