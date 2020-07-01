# -*- coding:utf-8 -*-
"""
自定义用户验证
"""
import requests
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户校验
    """
    def login_sso_system(self, username=None, password=None):
        sso_server = settings.SSO_SERVER_URL
        sso_url_login = "{}/api/v1/account/login".format(sso_server)
        data = {
            "username": username,
            "password": password
        }

        session = requests.Session()
        count = 0
        while count < 5:
            count += 1
            try:
                r = session.post(url=sso_url_login, data=data)
                result = r.json()
                if result["status"]:
                    # 登录成功: 获取用户信息
                    user = self.get_user_info(session=session)
                    return user

            except Exception as e:
                print(e)

    def get_user_info(self, session):
        """
        获取用户信息
        :param session: 登录后的ssion
        :return: 用户信息字典类型
        """
        sso_server = settings.SSO_SERVER_URL
        sso_url_info = "{}/api/v1/account/info".format(sso_server)

        count = 0
        while count < 5:
            count += 1
            try:
                r = session.get(url=sso_url_info)

                result = r.json()
                if result and result["id"] > 0:
                    return result
            except Exception as e:
                print(e)

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 去sso中登录账号
        user_info = self.login_sso_system(username=username, password=password)

        try:
            # 判断用户是否存在
            username = user_info["username"]
            user = User.objects.filter(username=username).first()
            if user:
                need_update = False
                for info_key in user_info:
                    info_keyvalue = user_info[info_key]
                    info_attr = getattr(user, info_key)
                    if info_attr != user_info[info_key]:
                        if not need_update:
                            need_update = True
                        setattr(user, info_key, info_keyvalue)

                # 判断是否需要更新
                if need_update:
                    user.save()
            else:
                # 新的用户，添加用户
                user = User.objects.create(**user_info)

            # 返回用户
            return user

        except Exception as e:
            return None
