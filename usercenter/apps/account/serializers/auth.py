# -*- coding:utf-8 -*-

from rest_framework import serializers


class AuthCheckSerializer(serializers.Serializer):
    """
    验证权限需要传递的数据
    """
    system = serializers.CharField(max_length=100, required=True)
    permission = serializers.CharField(max_length=100, required=True)

    class Meta:
        fields = ('system', 'permission')
