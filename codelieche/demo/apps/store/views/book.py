# -*- coding:utf-8 -*-
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from store.models.book import Book
from store.serializers.book import BookModelSerializer


class BookApiViewSet(ModelViewSet):
    queryset = Book.objects.filter(deleted=False)
    serializer_class = BookModelSerializer
    serializer_class_set = (BookModelSerializer,)
    # 测试环境用
    permission_classes = (AllowAny,)

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("title", "author", "description")
    filterset_fields = ("author", "price")
    ordering_fields = ("id", "author", "title", "price")
    ordering = ("id",)
