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
    def login_sso_system(self, request=None, username=None, password=None):
        # 安全日志：需要用到ip和设备名称
        ip = ""
        agent = ""
        for k in ["HTTP_X_REAL_IP", "REMOTE_ADDR"]:
            if k in request.META:
                ip = request.META[k]
                break
        if "HTTP_USER_AGENT" in request.META:
            agent = request.META["HTTP_USER_AGENT"]

        # 登录sso需要传递的参数
        data = {
            "username": username,
            "password": password
        }

        # 通过GET参数传递ip和agent是有伪装风险的，后续可优化
        sso_server = settings.SSO_SERVER_URL
        sso_url_login = "{}/api/v1/account/login?ip={}&agent={}".format(sso_server, ip, agent)

        # session是发起当前请求的会话
        session = requests.Session()
        count = 0
        while count < 5:
            count += 1
            try:
                r = session.post(url=sso_url_login, data=data)
                result = r.json()
                if result["status"]:
                    # 登录sso成功了：需要把ssosessionid设置到cookie中
                    ssosessionid = session.cookies.get("ssosessionid")
                    setattr(request, "need_set_ssosessionid", ssosessionid)
                    # 添加了need_set_ssosessionid的属性之后
                    # utils.middlewares.sso.CheckTicketMiddleware的处理process的时候就会设置cookie

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
        user_info = self.login_sso_system(request=request, username=username, password=password)

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
