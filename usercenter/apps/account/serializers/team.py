# -*- coding:utf-8 -*-
from rest_framework import serializers

from codelieche.tools.password import random_password
from account.models.user import User
from account.models.team import Team
from account.signals.team import team_create_signal


class TeamModelSerializer(serializers.ModelSerializer):
    """
    Team Model Serializer
    """
    code = serializers.CharField(required=False, allow_null=True)
    owner = serializers.SlugRelatedField(slug_field="username", many=False, allow_null=True,
                                         queryset=User.objects.all(), required=False)
    users = serializers.SlugRelatedField(slug_field="username", many=True, queryset=User.objects.all(), required=False)

    def validate(self, attrs):

        return attrs

    def create(self, validated_data):
        # 1. 检查code
        if 'code' not in validated_data or not validated_data['code']:
            validated_data['code'] = "{}{}".format(random_password(8).lower(), Team.strftime())

        # 2. 设置owner
        user = self.context['request'].user
        if 'user' not in validated_data or not validated_data['user']:
            validated_data['owner'] = user

        # 3. 调用创建方法
        instance = super().create(validated_data=validated_data)

        # 4. 发送创建信号：创建默认的项目角色
        team_create_signal.send(sender=instance)

        return instance

    class Meta:
        model = Team
        fields = (
            "id", "code", "name", "owner", "users", "logo", "description", "config", "is_active",
            "time_added"
        )
