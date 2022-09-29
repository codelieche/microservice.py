# -*- coding:utf-8 -*-
import json

from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse

from account.models.user import User, AnonymousUser


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = AnonymousUser()

        authorization_token = request.META.get('HTTP_AUTHORIZATION')
        TOKEN_PREFIX = "Bearer "
        if authorization_token and authorization_token.find(TOKEN_PREFIX) == 0:
            authorization_token = authorization_token[len(TOKEN_PREFIX):]

        if authorization_token:
            success, data = User.decode_jwt_token(token=authorization_token)
            if success:
                if isinstance(data, dict) and data.get('username'):
                    username = data['username']
                    # 提升效率，不从数据库中获取用户，直接根据解密出的数据，实例化用户

                    u = User.objects.filter(username=username).first()
                    if u:
                        user = u
                    # user = User(
                    #     id=data['id'], username=username,
                    #     is_active=data['is_active'], is_superuser=data['is_superuser'])
            else:
                content = {
                    'error': 401,
                    'status': False,
                    'message': 'Auth Error: {}'.format(data)
                }
                return HttpResponse(content=json.dumps(content), content_type="application/json", status=401)
        # 判断是否传递了x-team-id
        team_id = request.META.get('HTTP_X_TEAM_ID')
        if team_id:
            user.team_id = team_id
        # 如果没传递team_id就会从User中获取
        # print(user.team_id, team_id)
        # 设置user
        request.user = user

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     print("process_view middleware")
    #     return view_func(request, *view_args, **view_kwargs)
