# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models.permission import Permission


class PermissionModelSerializer(serializers.ModelSerializer):
    """
    Permission Model Serializer
    """

    def update(self, instance, validated_data):
        # 权限创建后，其绑定的系统是不可以修改的
        if validated_data.get('system'):
            validated_data['system'] = instance.system
        return super().update(instance=instance, validated_data=validated_data)

    class Meta:
        model = Permission
        fields = (
            "id", "system", "code", "name", "description", "time_added"
        )
