#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from json import load
from time import strftime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View

from .forms import *
from .models import Account


# Create your views here.


class BaseView(View):
    """ """

    context = {
        "runningYear": strftime("%Y"),
    }


class IndexView(BaseView):
    """ """

    def get(self, request):
        """

        :param request:
        :return:
        """
        return render(request, "index.html", context=self.context)


class AboutView(BaseView):
    """ """

    def get(self, request):
        """

        :param request:
        :return:
        """
        context = self.context
        context["licenses"] = load(open("licenses.json", encoding="utf-8"))
        return render(request, "about.html", context=context)


class LoginView(BaseView):
    """登录视图"""

    def get(self, request):
        """
        处理 GET 请求，显示登录表单
        :param request:
        :return:
        """
        context = self.context
        form = LoginForm()
        context["form"] = form
        return render(request, "login.html", context=context)

    def post(self, request):
        """
        处理 POST 请求，验证表单并登录用户
        :param request:
        :return:
        """
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request=request, username=data["username"], password=data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                # 用户认证失败，添加错误信息
                messages.error(request, "用户名或密码错误")
                context = self.context
                context["form"] = form
                return render(request, "login.html", context=context)
        else:
            # 表单验证失败，显示表单错误
            messages.error(request, "表单验证失败，请检查输入信息是否正确")
            context = self.context
            context["form"] = form
            return render(request, "login.html", context=context)


class RegisterView(BaseView):
    """用户注册视图"""

    def get(self, request):
        context = self.context
        form = RegistrationForm()
        context["form"] = form
        return render(request, "register.html", context=context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if self.username_exists(data["username"]):
                form.add_error("username", "用户名已存在")
            elif not self.passwords_match(data["password"], data["password1"]):
                form.add_error("password1", "两次输入的密码不一致")
            else:
                new_user = Account.objects.create_user(
                    username=data["username"], password=data["password1"]
                )
                login(request, new_user)
                return redirect("index")
        else:
            # 表单验证失败时添加消息提示
            messages.error(request, "表单验证失败，请检查输入信息是否正确。")
        context = self.context
        context["form"] = form
        return render(request, "register.html", context=context)

    def username_exists(self, username):
        """检查用户名是否存在"""
        return Account.objects.filter(username=username).exists()

    def passwords_match(self, password1, password2):
        """检查两次输入的密码是否一致"""
        return password1 == password2


def logout_view(request):
    logout(request)
    return redirect("index")
