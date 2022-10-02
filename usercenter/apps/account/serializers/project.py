# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models.user import User
from account.models.team import Team
from account.models.project import Project, ProjectRole, ProjectUser


class ProjectRoleModelSerializer(serializers.ModelSerializer):
    """
    Project Role Model Serializer
    """
    team = serializers.SlugRelatedField(slug_field="code", queryset=Team.objects.filter(deleted=False), required=True)
    team_name = serializers.ReadOnlyField(source="team.name")

    def create(self, validated_data):
        if not validated_data.get("name"):
            validated_data["name"] = validated_data["code"]

        return super().create(validated_data=validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('team'):
            validated_data['team'] = instance.team
        return super().update(instance=instance, validated_data=validated_data)

    class Meta:
        model = ProjectRole
        fields = ("id", "team", "team_name", "code", "name", "description", "time_added")


class ProjectUserModelSerializer(serializers.ModelSerializer):
    """
    Project User Model Serializer
    """

    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), required=True)

    project_name = serializers.ReadOnlyField(source="project.name")
    role_name = serializers.ReadOnlyField(source="role.name")
    team_id = serializers.ReadOnlyField(source="project.team_id")

    # def validated_user(self, value):
    #     pass

    # serializers.UniqueTogetherValidator

    def validate(self, attrs):
        try:
            project = attrs['project']
            role = attrs['role']
            if role.team != project.team:
                raise ValueError("请选择自己团队的角色")
                # raise serializers.ValidationError("只可绑定自己团队的角色")

            return attrs
        except Exception as e:
            raise serializers.ValidationError("校验出错：{}".format(str(e)))

    class Meta:
        model = ProjectUser
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ProjectUser.objects.filter(deleted=False),
                fields=('project', 'user', 'role'),
                message="当前用户已加入项目"
            )
        ]
        fields = ("id", "project", "project_name", "user", "role", "role_name", "team_id" , "time_added")


class ProjectUserInfoSerializer(serializers.ModelSerializer):
    """
    Project User Info Serializer
    """

    user = serializers.SlugRelatedField(slug_field="username", required=False, read_only=True)
    project = serializers.ReadOnlyField(source="project.code")
    role = serializers.ReadOnlyField(source="role.code")

    class Meta:
        model = ProjectUser
        fields = ("id", "project", "user", "role", "time_added")


class ProjectModelSerializer(serializers.ModelSerializer):
    """
    Project Model Serializer
    """
    owner = serializers.SlugRelatedField(slug_field="username", required=False, allow_null=True,
                                         queryset=User.objects.all())
    team = serializers.SlugRelatedField(slug_field="code", required=True, queryset=Team.objects.all())
    team_name = serializers.ReadOnlyField(source="team.name")

    users = ProjectUserInfoSerializer(source="projectuser_set", many=True, allow_null=True, read_only=True)

    def create(self, validated_data):
        if not validated_data.get("name"):
            validated_data["name"] = validated_data["code"]

        return super().create(validated_data=validated_data)

    def create(self, validated_data):
        if not validated_data.get('owner'):
            user = self.context['request'].user
            validated_data['owner'] = user
        return super().create(validated_data=validated_data)

    def update(self, instance, validated_data):
        # 修改的时候team是不可改变的
        if validated_data.get('team'):
            validated_data['team'] = instance.team
        return super().update(instance=instance, validated_data=validated_data)

    class Meta:
        model = Project
        fields = (
            "id", "team", "team_name", "code", "name", "description", "owner", "users", "is_active",
            "time_added"
        )

