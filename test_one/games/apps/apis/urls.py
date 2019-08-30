'''
filename = urls.py
author = ZKY
date = 2019/08/06
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    # 短信验证码
    url(r'^mobile_captcha/$', views.get_mobile_captcha, name="mobile_captcha"),
    # 图片验证码
    url(r'^get_captcha/$', views.get_captcha, name='get_captcha'),
    # 检查验证码
    url(r'^check_captcha/$', views.check_captcha, name='check_captcha'),
    # 修改头像
    url(r'^change_avator/$', views.ChangeAvator.as_view(), name='change_avator'),
    #
    url(r'^games_list/$', views.ListView.as_view(), name='games_list'),
]