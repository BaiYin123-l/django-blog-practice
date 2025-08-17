#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
from django.contrib import admin

# Register your models here.
from core.models import Post, Profile, Comment, LikePost, LikeComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin): ...


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): ...


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin): ...


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin): ...


@admin.register(LikeComment)
class LikeCommentAdmin(admin.ModelAdmin): ...
