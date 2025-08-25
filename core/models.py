#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import AbstractUser, User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Account(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatar",
        null=True,
        blank=True,
        default="avatar/default.svg",
        verbose_name="Avatar"
    )
    bio = models.TextField(
        null=True,
        blank=True,
        max_length=500,
        default="No bio.",
        verbose_name="Bio"
    )

    def __str__(self):
        return self.username

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'core':  # 替换为你的应用名称
        # 获取 Post 模型的 ContentType
        content_type = ContentType.objects.get_for_model(Post)

        # 创建普通用户组
        regular_user_group, created = Group.objects.get_or_create(name='Regular User')
        regular_user_group.permissions.add(
            Permission.objects.get(codename='add_post', content_type=content_type),
            Permission.objects.get(codename='change_post', content_type=content_type)
        )

        # 创建审核组
        reviewer_group, created = Group.objects.get_or_create(name='Reviewer')
        reviewer_group.permissions.add(
            Permission.objects.get(codename='change_post', content_type=content_type),
            Permission.objects.get(codename='delete_post', content_type=content_type)
        )

        # 创建管理组
        admin_group, created = Group.objects.get_or_create(name='Admin')
        admin_group.permissions.add(
            Permission.objects.get(codename='add_post', content_type=content_type),
            Permission.objects.get(codename='change_post', content_type=content_type),
            Permission.objects.get(codename='delete_post', content_type=content_type),
            Permission.objects.get(codename='view_post', content_type=content_type)
        )


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_tags(sender, **kwargs):
    if sender.name == "core":  # 替换为你的应用名称
        if Tag.objects.count() == 0:
            print(1)
            Tag.objects.create(name="live")
            Tag.objects.create(name="learn")


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field()
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def like_count(self):
        return self.likepost_set.filter(status=True).count()

    def __str__(self):
        return self.title


class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} like {self.post} {self.status}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.status
