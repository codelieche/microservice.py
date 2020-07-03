# -*- coding:utf-8 -*-
"""
生成rest_framework想过的token
"""
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from account.serializers.token import ObtainJwtTokenSerializer


class ObainRestFrameworkAuthTokenApiView(APIView):
    """
    获取访问token的api View
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # 判断用户权限
        if user.has_perm("account.can_use_token"):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'status': True, 'token': token.key})
        else:
            return Response({"status": False, "message": "当前用户无权限使用Token"}, status=403)


class JwtTokenObtainPairView(TokenViewBase):
    """
    JWT申请Token的api view
    参考：rest_framework_simplejwt.views.TokenObtainPairView
    """
    serializer_class = ObtainJwtTokenSerializer
