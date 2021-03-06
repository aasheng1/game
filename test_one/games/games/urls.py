"""games URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from .settings import MEDIA_ROOT
from apps.accounts import views

urlpatterns = [
    # 后台管理
    url(r'^admin/', admin.site.urls),
    # 主页
    # url(r'^$',TemplateView.as_view(template_name='accounts/index.html'),name="index"),
    url(r'^$',views.index,name="index"),
    # 进入用户
    url(r'^accounts/',include("apps.accounts.urls",namespace="accounts")),
    # 下载
    url(r'^download/',include("apps.download.urls",namespace="download")),
    # api接口
    url(r'^apis/', include('apps.apis.urls', namespace="apis")),
    # 用户中心
    url(r'^uc/', include('apps.usercenter.urls', namespace="uc")),
    # media图片路由处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 用户中心路由
]
