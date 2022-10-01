# -*- coding:utf-8 -*-
from rest_framework import serializers
from django.db.models import Q

from account.models.role import Role
from account.models.system import System
from account.models.team import Team


class RoleModelSerializer(serializers.ModelSerializer):
    """
    Role Model Serializer
    """
    system = serializers.SlugRelatedField(slug_field="code", required=False,
                                          queryset=System.objects.filter(deleted=False), allow_null=True)
    team = serializers.SlugRelatedField(slug_field="code", required=False,
                                        queryset=Team.objects.filter(deleted=False), allow_null=True)

    def check_code_isexist(self, code, instance=None):
        user = self.context['request'].user
        if instance:
            if Role.objects.filter(Q(code=code, team=None) | Q(code=code, team_id=user.team_id)).exclude(id=instance.id).count() > 0:
                raise serializers.ValidationError('{}角色已经存在'.format(code))
        else:
            if Role.objects.filter(Q(code=code, team=None) | Q(code=code, team_id=user.team_id)).count() > 0:
                raise serializers.ValidationError('{}角色已经存在'.format(code))

    def create(self, validated_data):
        if not validated_data.get("name"):
            validated_data["name"] = validated_data["code"]
        # 需要检查一下code
        code = validated_data["code"]
        self.check_code_isexist(code=code)

        return super().create(validated_data=validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('team'):
            validated_data['team'] = instance.team

        # 需要检查一下code
        if 'code' in validated_data:
            code = validated_data["code"]
            self.check_code_isexist(code=code, instance=instance)

        return super().update(instance=instance, validated_data=validated_data)

    class Meta:
        model = Role
        fields = (
            "id", "system", "team", "team_name", "code", "name", "permissions", "description", "time_added"
        )
