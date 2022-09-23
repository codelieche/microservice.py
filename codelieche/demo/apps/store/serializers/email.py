# -*- coding:utf-8 -*-
from rest_framework import serializers

from store.models.email import Email


class EmailModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ("id", "platform", "name", "password", "time_added")
