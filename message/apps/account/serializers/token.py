# -*- coding:utf-8 -*-

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class ObtainJwtTokenSerializer(TokenObtainSerializer):
    """
    申请JWT的Token序列化
    参考：rest_framework_simplejwt.serializers.TokenObtainPairSerializer
    """

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        # 获取到了用户后，判断其是否可以访问本系统
        # 后续需要指定权限的账号，才可以使用JWT TOKEN
        if self.user.can_view:
            refresh = self.get_token(self.user)

            data["status"] = True
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            return data
        else:
            # 当前用户不可访问本系统
            data["status"] = False
            data["message"] = "用户({})不能访问本系统，请找管理员开通访问权限".format(self.user.username)

            return data
