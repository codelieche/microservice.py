# -*- coding:utf-8 -*-
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from store.models.todolist import TodoList
from store.serializers.todolist import TodoListModelSerializer


class TodoListApiViewSet(ModelViewSet):
    queryset = TodoList.objects.filter(deleted=False)
    serializer_class = TodoListModelSerializer
    serializer_class_set = (TodoListModelSerializer,)
    # 测试环境用
    permission_classes = (AllowAny,)

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("title",)
    filterset_fields = ("title", "time_added")
    ordering_fields = ("id", "time_added", "time_finished")
    ordering = ("id",)
