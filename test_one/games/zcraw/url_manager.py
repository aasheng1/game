import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "games.settings")  # website可以更改为自己的项目名称
django.setup()  # Django版本大于1.7 加入这行代码

class UrlManager(object):
    # 在各个函数进行初始化
    def __init__(self):
        self.new_urls = list()
        self.old_urls = list()
        self.class_new_urls = list()
        self.class_old_urls = list()

    # 向管理器中添加url
    def add_new_url(self, url):
        if url is None:
            return
        # 判断url既不在待爬取的url里，也不再爬取过的url里
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.append(url)

    # 向管理器中添加批量url
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    # 判断管理器中是否有新的待爬取的url
    def has_new_url(self):
        return len(self.new_urls) != 0


    # 从url管理器中获取一个新的待爬取的url
    def get_new_url(self):
        new_url = self.new_urls.pop(0)
        self.old_urls.append(new_url)
        return new_url





    # 增加分类页面的网址
    def add_class_urls(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_class_url(url)

    # 向管理器中添加url
    def add_class_url(self, url):
        if url is None:
            return
        # 判断url既不在待爬取的url里，也不再爬取过的url里
        if url not in self.class_new_urls and url not in self.class_old_urls:
            self.class_new_urls.append(url)

    def has_class_url(self):
        return len(self.class_new_urls) != 0

    # 从url管理器中获取一个新的待爬取的url
    def get_class_url(self):
        new_url = self.class_new_urls.pop(0)
        self.class_old_urls.append(new_url)
        return new_url
