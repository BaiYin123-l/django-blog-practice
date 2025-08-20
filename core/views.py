#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import random
from json import load
from time import strftime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from .forms import *
from .models import *


# Create your views here.


class BaseView(View):
    """ """

    context = {
        "runningYear": strftime("%Y"),
    }


class IndexView(BaseView):
    """首页视图，实现随机推荐功能"""

    def get(self, request):
        """
        首页视图的 GET 方法，实现随机推荐帖子
        :param request: 请求对象
        :return: 渲染后的首页
        """
        context = self.context

        # 获取所有帖子
        posts = Post.objects.all()

        # 计算每个帖子的权重并打乱顺序
        weighted_posts = self.get_weighted_posts(posts)

        # 将打乱后的帖子列表添加到上下文中
        context["posts"] = weighted_posts

        return render(request, "index.html", context=context)

    @staticmethod
    def get_weighted_posts(posts, alpha=0.5, beta=0.5):
        """
        计算每个帖子的权重并打乱顺序
        :param posts: Post 对象列表
        :param alpha: 时间权重系数
        :param beta: 点赞权重系数
        :return: 打乱后的帖子列表
        """
        current_time = timezone.now()
        weighted_posts = []

        for post in posts:
            # 计算时间权重
            time_diff = (current_time - post.created_at).days + 1  # 防止除以0
            time_weight = 1 / time_diff

            # 计算点赞权重
            like_weight = post.like_count

            # 计算总权重
            total_weight = alpha * time_weight + beta * like_weight

            weighted_posts.append((post, total_weight))

        # 根据权重打乱帖子顺序
        # 使用 random.sample 按权重随机选择帖子
        posts_only = [post for post, weight in weighted_posts]
        weights = [weight for post, weight in weighted_posts]

        # 随机选择帖子，权重高的帖子有更高的概率被选中
        # 使用 random.sample 确保不重复
        shuffled_posts = random.sample(posts_only, k=len(posts_only))

        return shuffled_posts

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


def username_exists(username):
    """检查用户名是否存在"""
    return Account.objects.filter(username=username).exists()


def passwords_match(password1, password2):
    """检查两次输入的密码是否一致"""
    return password1 == password2


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
            if username_exists(data["username"]):
                form.add_error("username", "用户名已存在")
            elif not passwords_match(data["password"], data["password1"]):
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


def logout_view(request):
    logout(request)
    return redirect("index")


class SettingsView(BaseView):
    def get(self, request):
        context = self.context
        return render(request, "settings.html", context=context)


class SettingsHandleView(BaseView):
    def post(self, request, mode):
        if mode == "password":
            return self.handle_password(request)
        elif mode == "avatar":
            return self.handle_avatar(request)
        elif mode == "signature":
            return self.handle_signature(request)
        else:
            return HttpResponse("Invalid mode", status=400)

    def handle_password(self, request):
        password1, password2 = request.POST.get("password1"), request.POST.get(
            "password2"
        )
        if password1 or password2:
            if passwords_match(password1, password2):
                request.user.set_password(password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                self.context["password_message"] = "Password updated successfully"
                return render(request, "settings.html", context=self.context)
            else:
                self.context["password_message"] = "Password did not match"
                return render(request, "settings.html", context=self.context)
        else:
            self.context["password_message"] = "Password was not changed"
        return render(request, "settings.html", context=self.context)

    def handle_avatar(self, request):
        avatar = request.FILES.get("avatar")
        if avatar:
            # 保存头像逻辑
            request.user.avatar = avatar
            request.user.save()
            self.context["avatar_message"] = "Avatar updated successfully"
        else:
            self.context["avatar_message"] = "Avatar was not changed"
        return render(request, "settings.html", context=self.context)

    def handle_signature(self, request):
        signature = request.POST.get("signature")
        if signature:
            # 保存个人签名逻辑
            request.user.bio = signature
            request.user.save()
            self.context["signature_message"] = "Signature updated successfully"
        else:
            self.context["signature_message"] = "Signature was not changed"
        return render(request, "settings.html", context=self.context)


def deregister(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            logout(request)
            user.delete()
            return redirect("index")
        else:
            messages.info(request, "未登录")
            return redirect("index")


@method_decorator(login_required, name="dispatch")
class PostEditView(BaseView):
    def get(self, request, post_id=None):
        context = self.context
        if post_id:
            post = Post.objects.get(pk=post_id)
            form = PostForm(instance=post)
        else:
            form = PostForm()
        context["form"] = form
        return render(request, "edit.html", context=context)

    def post(self, request, post_id=None):
        if post_id:
            post = Post.objects.get(pk=post_id)
            form = PostForm(request.POST, instance=post)
        else:
            form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)  # 不立即保存到数据库
            post.author = request.user  # 设置当前登录用户为作者
            post.save()  # 保存到数据库
            form.save_m2m()  # 保存多对多字段
            return redirect("index")  # 替换为成功后的跳转地址
        else:
            context = self.context
            context["form"] = form
            return render(request, "edit.html", context=context)

class PostView(BaseView):
    def get(self, request, post_id):
        context = self.context
        post = Post.objects.get(id=post_id)
        context["post"] = post
        return render(request, "read.html", context=context)