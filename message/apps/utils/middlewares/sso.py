# -*- coding:utf-8 -*-
"""
sso相关的中间件
"""
import requests

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import login

from account.models import User


class CheckTicketMiddleware(MiddlewareMixin):
    """
    检查请求中是否包含ticket的中间件
    """

    def check_sso_ticket(self, ticket):
        """
        检查sso的ticket
        :param ticket: 登录券
        :return:
        """
        sso_server = "http://127.0.0.1:8000"
        sso_url_check_ticket = "{}/api/v1/account/ticket/check?ticket={}".format(sso_server, ticket)

        count = 0
        while count < 5:
            count += 1
            try:
                r = requests.get(url=sso_url_check_ticket)
                result = r.json()
                if "status" in result and result["status"]:
                    if "data" in result:
                        user_info_and_session = result["data"]
                        return user_info_and_session
            except Exception as e:
                print(e)

    def process_request(self, request):
        if request.method == "GET":
            ticket = request.GET.get("ticket")

            # 如果没用户登录，才使用ticket
            if ticket and not request.user.is_authenticated:
                user_info_and_session = self.check_sso_ticket(ticket=ticket)
                try:
                    if user_info_and_session and "user" in user_info_and_session:
                        user_info = user_info_and_session["user"]

                        # 更新用户数据或者添加用户
                        user = User.objects.filter(username=user_info["username"]).first()
                        if user is not None:
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

                        # 如果没用户登录，才使用ticket
                        if not request.user.is_authenticated and user.can_view:
                            # 登录用户
                            login(request, user)
                            # 设置Cookie：ssosessionid
                            ssosessionid = user_info_and_session["sessionid"]
                            setattr(request, "need_set_ssosessionid", ssosessionid)

                            # 记录数据到sso: 最好是异步
                            # request.session.session_key 系统名称

                except Exception as e:
                    return
        # 不是GET的方法
            # 未传递ticket的参数

    def process_response(self, request, response):
        """处理Response"""
        # 判断是否需要设置ssosessionid的Cookie
        ssosessionid = getattr(request, "need_set_ssosessionid", None)
        if ssosessionid:
            response.set_cookie("ssosessionid", ssosessionid)

        return response
