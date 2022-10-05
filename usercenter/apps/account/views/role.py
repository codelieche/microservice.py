# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from codelieche.django.views.mixins import BatchActionMixin

from account.models.role import Role
from account.serializers.role import RoleModelSerializer


class RoleApiViewSet(BatchActionMixin, ModelViewSet):
    """
    Role Api View Set
    """
    queryset = Role.objects.filter(deleted=False)
    serializer_class = RoleModelSerializer
    serializer_class_set = (RoleModelSerializer,)
    permission_classes = (IsAuthenticated,)

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("system__name", "name")
    filterset_fields = ("system", "team", "name")
    ordering_fields = ("id", "system", "team", "name")
    ordering = ("id",)

    def update(self, request, *args, **kwargs):
        r = super().update(request=request, *args, **kwargs)
        return r

