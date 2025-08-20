#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
from django.urls import path

from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("settings/<str:mode>/", SettingsHandleView.as_view(), name="SettingsHandle"),
    path("deregister/", deregister, name="deregister"),
    path("post/edit", PostEditView.as_view(), name="post-edit"),
    path("post/<int:post_id>/", PostView.as_view(), name="post"),
path('review/', review_view, name='review'),
    path('get_post/<int:post_id>/', get_post, name='get_post'),
    path('approve_post/<int:post_id>/', approve_post, name='approve_post'),
    path('unapprove_post/<int:post_id>/', unapprove_post, name='unapprove_post'),
]
