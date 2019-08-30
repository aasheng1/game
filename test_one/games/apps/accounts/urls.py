from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    # url(r'^$',views.index,name="index"),
    # 登录
    url(r'^login/',views.Login.as_view(),name="login"),
    # 测试网站
    url(r'^login_test/',views.login_test,name="login_test"),
    # 注册
    url(r'register/',views.Register.as_view(),name="register"),
    # 登出
    url(r'logout/$', views.logout, name="logout"),
    # 发送邮件
    url(r'sendemail/', views.Email_check.as_view(), name='sendemail')
]