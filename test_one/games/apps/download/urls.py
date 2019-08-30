from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'^$',views.classify),
    # 列出分类游戏
    url(r'^list/',views.Download_list,name="list"),
    # 游戏分类界面
    url(r'^classify/',views.Download_classify,name="classify"),
    # 游戏详情
    url(r'^details/(?P<id>\d+)/$',views.Download_details,name="download_details"),
    # 游戏分类下拉
    url(r'^sort(?P<pk>\d+)/',views.Sort,name="sort"),
]