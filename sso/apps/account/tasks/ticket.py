# -*- coding:utf-8 -*-
import random
import datetime

from account.models.ticket import Ticket


def generate_ticket(request):
    """
    生成登录券
    :param request: http的请求
    :return:
    """
    # 第1步：判断相关信息
    # 1-1：判断用户是否登录
    user = request.user
    if not user.is_authenticated:
        return None

    # 1-2: 判断是否有returnUrl
    return_url = request.GET.get("returnUrl")
    if not return_url:
        return None

    # 1-3: 判断是否有sessionID
    ssosessionid = request.COOKIES.get("ssosessionid")
    if not ssosessionid:
        return None

    # 第2步：生成当前ticket的name
    now = datetime.datetime.now()
    ticket_name = "{}{}{}".format(now.strftime("%Y%m%d%H%M%S"), user.id, random.randint(100, 1000))

    # 第3步：创建ticket
    ticket = Ticket.objects.create(
            user=user, sessionid=ssosessionid, name=ticket_name, return_url=return_url,
            is_active=True, time_expired=now + datetime.timedelta(seconds=60)
        )

    # 第4步：返回登录券
    return ticket
