# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """
    User Model Serializer
    """

    def create(self, validated_data):
        request = self.context["request"]
        # 密码校验
        password = request.data.get("password")
        re_password = request.data.get("re_password")

        if password and re_password:
            if password != re_password:
                raise serializers.ValidationError("密码和确认密码不相同")
        else:
            raise serializers.ValidationError("请输入密码和确认密码")

        instance = super().createe(validated_data=validated_data)

        # 设置密码
        instance.set_password(password.strip())
        instance.nick_name = instance.username
        # 注册的用户都需要管理员，手动设置其是否可访问本系统
        instance.can_view = False
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("id", "username", "nick_name", "mobile", "email", "qq", "wechart", "dingding")


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录 Serializer
    """
    username = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(max_length=40, required=True)

