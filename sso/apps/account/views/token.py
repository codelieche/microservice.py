# -*- coding:utf-8 -*-
"""
生成rest_framework想过的token
"""
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models.safelog import SafeLog


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

        # 安全日志：需要用到ip和设备名称
        ip = "---"
        agent = "---"
        for k in ["HTTP_X_REAL_IP", "REMOTE_ADDR"]:
            if k in request.META:
                # meta = request.META
                # print(meta)
                ip = request.META[k]
                break
        if "HTTP_USER_AGENT" in request.META:
            agent = request.META["HTTP_USER_AGENT"]

        # 判断用户权限
        if user.has_perm("account.can_use_token"):
            token, created = Token.objects.get_or_create(user=user)

            # 记录安全日志：safe
            if created:
                safelog_content = "申请DRF TOKEN成功"
                SafeLog.objects.create(user=user, content=safelog_content, category="safe", ip=ip, devices=agent,
                                       success=True)
            else:
                safelog_content = "申请DRF TOKEN成功:(已存在Token)"
                SafeLog.objects.create(user=user, content=safelog_content, category="safe", ip=ip, devices=agent,
                                       success=True)

            return Response({'status': True, 'token': token.key})
        else:
            if user and getattr(user, "id") and getattr(user, "id") > 0:
                safelog_content = "申请DRF TOKEN失败：无权限"
                SafeLog.objects.create(user_id=getattr(user, "id"), content=safelog_content, category="safe", ip=ip, devices=agent,
                                       success=False)
            return Response({"status": False, "message": "当前用户无权限使用Token"}, status=403)
