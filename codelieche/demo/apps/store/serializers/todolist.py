# -*- coding:utf-8 -*-
from rest_framework import serializers

from store.models.todolist import TodoList


class TodoListModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoList
        fields = ("id", "title", "done", "time_added", "time_updated", "time_finished")
