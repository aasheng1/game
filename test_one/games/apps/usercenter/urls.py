'''
filename = urls.py
author = LJH
date = 2019/08/19
'''

from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from django.views.static import serve
from games.settings import MEDIA_ROOT

urlpatterns = [
    # 个人资料
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    # media图片路由处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 修改密码
    url(r'^change_passwd/$', views.ChangePasswdView.as_view(), name='change_passwd'),
    # 找回密码邮箱路由
    url(r'password/forget/$', views.PasswordForget.as_view(), name="password_forget"),
    # 重置密码
    url(r'password/reset/(\w+)/$', views.PasswordReset.as_view(), name="password_reset"),
    # 联系我
    url(r'password/callme',views.Callme,name="callme")
]