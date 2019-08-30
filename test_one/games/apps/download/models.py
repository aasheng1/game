from django.db import models


# Create your models here.
class GameClass(models.Model):
    type_name = models.CharField(verbose_name='游戏分类', max_length=128,null=True,unique=True)
    picture = models.CharField(verbose_name='游戏分类图片',max_length=128,null=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.type_name}"

class Publishers(models.Model):
    publistshers_name = models.CharField(verbose_name="游戏厂商",max_length=128,null=True,unique=True)

    class Meta:
        verbose_name = "游戏厂商"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.publistshers_name}"

# class Tag(models.Model):
#     name = models.CharField(verbose_name="标签",max_length=128)
#
#     class Meta:
#         verbose_name = "游戏标签"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return f"{self.name}"

class GameDetails(models.Model):
    game_name = models.CharField(verbose_name="游戏名称", max_length=128,null=True,unique=True)
    name_alias = models.CharField(verbose_name="游戏下载别名", max_length=256,null=True)
    poster = models.CharField(verbose_name="海报", max_length=256,null=True)
    grade = models.FloatField(verbose_name="游戏评分", max_length=10,null=True)
    introduce = models.TextField(verbose_name="游戏介绍", max_length=256,null=True)
    # url = models.(Url,verbose_name="Url链接")
    down_url = models.CharField(verbose_name="详情页链接链接", max_length=256,null=True)
    BT_link = models.CharField(verbose_name="BT链接", max_length=256,null=True)
    game_link = models.CharField(verbose_name="游戏下载地址",max_length=256,null=True)
    baiduyun = models.CharField(verbose_name="百度云下载地址",max_length=256,null=True)
    # tag = models.ManyToManyField(Tag, verbose_name="游戏标签")
    tag = models.CharField(max_length=256, verbose_name="游戏标签",null=True)
    sell = models.CharField(verbose_name="发售时间", max_length=256,null=True)
    gameclass = models.ForeignKey(GameClass,verbose_name="游戏类型", max_length=256,null=True)
    # gamclass = models.CharField(verbose_name="游戏类型", max_length=256,null=True)
    publishers = models.ForeignKey(Publishers, verbose_name="游戏厂商",max_length=256,null=True)
    # publishers = models.CharField(verbose_name="游戏厂商",max_length=256,null=True)
    size = models.CharField(verbose_name="游戏大小", max_length=256,null=True)

    picture_min = models.TextField(verbose_name="游戏截图缩略图",max_length=256,null=True)
    picture_max = models.TextField(verbose_name="游戏截图大图",max_length=256,null=True)

    class Meta:
        verbose_name = "游戏信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.game_name}"


