# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models.fields.files import ImageFieldFile
import os
from libs.images import make_thumb

# 继承自AbstractUser
class User(AbstractUser):
    # 如果定制User，需要在Settings配置AUTH_USER_MODEL
    # CharField => max_length
    # ImageFiled => Pillow 库
    username = models.CharField(max_length=20,verbose_name="用户名",unique=True)
    password = models.CharField(max_length=100,verbose_name="密码")
    # realname = models.CharField(max_length=8, verbose_name="真实姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机号",unique=True)
    email = models.EmailField(verbose_name="邮箱地址")
    avator_sor = ThumbnailerImageField(upload_to="avator/%Y%m%d/", default="avator/default.jpg", verbose_name="头像")
    #
    # def __str__(self):
    #     return self.username

    # class Meta:
    #     verbose_name = "用户列表"
    #     verbose_name_plural = verbose_name

