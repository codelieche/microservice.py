# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models.system import System
from account.signals.system import system_create_signal


class SystemModelSerializer(serializers.ModelSerializer):
    """
    System Model Serializer
    """

    def create(self, validated_data):
        if not validated_data.get("name"):
            validated_data["name"] = validated_data["code"]

        instance = super().create(validated_data=validated_data)
        # 发送创建信号：创建默认的角色
        system_create_signal.send(sender=instance)
        return instance

    class Meta:
        model = System
        fields = ("id", "code", "name", "description", "time_added")
