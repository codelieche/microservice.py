# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from account.models.permission import Permission
from account.serializers.permission import PermissionModelSerializer


class PermissionApiViewSet(ModelViewSet):
    """
    Permission Api View Set
    """
    queryset = Permission.objects.filter(deleted=False)
    serializer_class = PermissionModelSerializer
    serializer_class_set = (PermissionModelSerializer,)
    permission_classes = (IsAuthenticated,)

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("code", "name", "system__code")
    filterset_fields = ("code", "system", "name")
    ordering_fields = ("id", "system", "code", "name")
    ordering = ("id",)
