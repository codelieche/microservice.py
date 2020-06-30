# -*- coding:utf-8 -*-
"""
安全日志
"""
from rest_framework import serializers

from account.models.user import User
from account.models.safelog import SafeLog


class SafeLogModelSerializer(serializers.ModelSerializer):
    """
    安全日志序列化Model
    """
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category_verbose = serializers.CharField(read_only=True, required=False, source="get_category_display")

    class Meta:
        model = SafeLog
        fields = ("id", "user", "category", "content", "category_verbose", "ip", "devices", "success", "time_added")
