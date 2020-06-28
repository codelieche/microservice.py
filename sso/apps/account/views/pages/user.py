"""
网站首页
"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from account.forms.user import UserLoginForm


class UserLoginPageView(View):
    """
    用户登录
    """
    def get(self, request):
        url = request.get_full_path()
        next_url = request.GET.get("next")
        if next_url:
            return HttpResponseRedirect(redirect_to=next_url)

        form = UserLoginForm()
        return render(request, "user/login.html", {"form": form, 'url': url, 'user': request.user})

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
                        next_url = request.GET.get('next', '/user/login')
                        return HttpResponseRedirect(redirect_to=next_url)
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
                                                   'msg': message})


class UserLogoutPageView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        next_url = request.GET.get("next", "/user/login")
        return HttpResponseRedirect(redirect_to=next_url)
