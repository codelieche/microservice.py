# -*- coding:utf-8 -*-
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from store.models.email import Email
from store.serializers.email import EmailModelSerializer


class EmailApiViewSet(ModelViewSet):
    queryset = Email.objects.filter(deleted=False)
    # queryset = Book.objects.filter()
    serializer_class = EmailModelSerializer
    serializer_class_set = (EmailModelSerializer,)
    # 测试环境用
    permission_classes = (AllowAny,)

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("name", "platform")
    filterset_fields = ("platform", "name")
    ordering_fields = ("id", "platform", "name")
    ordering = ("id",)
