#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from captcha.fields import CaptchaField
from django.forms import *
from django_ckeditor_5.fields import CKEditor5Widget


class LoginForm(Form):
    username = CharField(required=True, label="用户名")
    password = CharField(widget=PasswordInput, required=True, label="密码")
    check = CaptchaField(label="验证码", required=True)


class RegistrationForm(Form):
    username = CharField(required=True, label="用户名")
    password = CharField(required=True, label="密码", widget=PasswordInput)
    password1 = CharField(required=True, label="重复密码", widget=PasswordInput)
    check = CaptchaField(label="验证码", required=True)


from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Post, Tag

class PostForm(ModelForm):
    title = CharField(label="标题", required=True)
    content = forms.CharField(widget=CKEditor5Widget, label="正文", required=True)
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="标签",
        required=False
    )

    class Meta:
        model = Post
        fields = ["title", "tags", "content"]

class CommentForm(Form):
    comment_id = CharField(required=False, label="")
    comment_input = CharField(required=True, label="")

