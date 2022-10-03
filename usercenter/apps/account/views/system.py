# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from account.models.system import System
from account.serializers.system import SystemModelSerializer


class SystemApiViewSet(ModelViewSet):
    """
    System Api View Set
    """
    queryset = System.objects.filter(deleted=False)
    serializer_class = SystemModelSerializer
    serializer_class_set = (SystemModelSerializer,)
    permission_classes = (IsAuthenticated,)

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("code", "name")
    filterset_fields = ("code", "name")
    ordering_fields = ("id", "code", "name")
    ordering = ("id",)

    # look up field
    # lookup_field = "id"

    # def get_object(self):
    #     # 兼容id和code的获取，如果code是
    #     if not self.kwargs['id'].isdigit():
    #         instance = System.objects.filter(code=self.kwargs['id']).first()
    #     else:
    #         instance = super().get_object()
    #     return instance
