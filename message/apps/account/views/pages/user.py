"""
网站首页
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings

from account.forms.user import UserLoginForm


class UserLoginPageView(View):
    """
    用户登录
    """
    def get(self, request):
        url = request.get_full_path()
        return_url = request.GET.get("returnUrl")
        user = request.user
        if user.is_authenticated and return_url:
            return HttpResponseRedirect(redirect_to=return_url)

        form = UserLoginForm()
        return render(request, "user/login.html", {
            "form": form, 'url': url, 'user': request.user,
            "sso_server_url": settings.SSO_SERVER_URL
        })

    def post(self, request):
        url = request.get_full_path()
        form = UserLoginForm(request.POST)
        if form.is_valid():
            form_cleaned = form.cleaned_data
            user = authenticate(username=form_cleaned['username'],
                                password=form_cleaned['password'])
            if user is not None:
                # 判断用户是否是激活的
                if user.is_active:
                    if user.can_view:
                        login(request, user)
                        return_url = request.GET.get('returnUrl', '/user/login')

                        return HttpResponseRedirect(redirect_to=return_url)
                    else:
                        message = "用户({})，不可访问本系统，请联系管理员开通".format(user.username)
                else:
                    message = "用户已经被禁用"
                    # return HttpResponse('{sucess:false}')
            else:
                message = "用户名或者密码错误"
        else:
            # 数据清理后，不符合要求
            message = "输入的内容不合法"
        return render(request, 'user/login.html', {'form': form,
                                                   'url': url,
                                                   'msg': message,
                                                   "sso_server_url": settings.SSO_SERVER_URL
                                                   })


@method_decorator(
    login_required(login_url=settings.SSO_SERVER_LOGIN_URL, redirect_field_name=settings.REDIRECT_FIELD_NAME),
    name="dispatch"
)
class UserInfoPageView(View):
    """
    用户信息页：仅为了测试
    """
    def get(self, request):
        # 获取到用户:
        user = request.user

        msg = "当前系统：{}".format(settings.CURRENT_SERVICE_CODE)
        return render(request, "user/info.html", {
            "user": user, "msg": msg,
            "sso_server_url": settings.SSO_SERVER_URL
        })


class UserLogoutPageView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        next_url = request.GET.get("next", settings.SSO_SERVER_LOGIN_URL)
        return HttpResponseRedirect(redirect_to=next_url)
