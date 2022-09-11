# -*- coding:utf-8 -*-
from rest_framework import serializers

from store.models.book import Book


class BookModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ("id", "title", "author", "price", "store", "description", "time_added")
