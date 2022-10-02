# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from account.models.team import Team
from account.serializers.team import TeamModelSerializer


class TeamApiViewSet(ModelViewSet):
    """
    Team Api View Set
    """
    queryset = Team.objects.filter(deleted=False)
    serializer_class = TeamModelSerializer
    serializer_class_set = (TeamModelSerializer,)
    permission_classes = (IsAuthenticated,)

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("owner__username", "name")
    filterset_fields = ("owner", "name", "code")
    ordering_fields = ("id", "owner", "name")
    ordering = ("id",)
