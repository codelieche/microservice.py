# -*- coding:utf-8 -*-
"""
自定义用户验证
"""

from rest_framework.authentication import BaseAuthentication
from account.models.user import User


class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # return User.objects.first(), True
        if request._request.user:
            return request._request.user, True
        else:
            return None

    def authenticate_header(self, request):
        return "Authorization"
