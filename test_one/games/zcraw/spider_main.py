# coding=utf-8
import time, datetime
import re
import urllib
from urllib.parse import urlparse
import django
import os
from zcraw import url_manager, html_downloader, html_parser, html_outputer
from apps.download.models import GameDetails

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "games.settings")  # website可以更改为自己的项目名称
django.setup()  # Django版本大于1.7 加入这行代码


class Spider_Main(object):
    #初始化操作
    def __init__(self):
        #设置url管理器
        self.urls = url_manager.UrlManager()
        #设置HTML下载器
        self.downloader = html_downloader.HtmlDownloader()
        #设置HTML解析器
        self.parser = html_parser.HtmlParser()
        #设置HTML输出器
        self.outputer = html_outputer.HtmlOutputer()

    #爬虫调度程序
    def craw(self, root_url):
        y = 0
        # 循环要爬取的网站，URL不变，仅在后面加上数字
        for i in range(3,5):
            # 获得进入的入口
            url_cycle = f'https://www.ali213.net/zt/ztisitemap_sale_p{i}.html'
            new_full_url = urllib.parse.urljoin(root_url, url_cycle)
            # 按网站规律将所有要爬取的网站放入一个列表里
            self.urls.add_class_url(new_full_url)
        # 将存入列表里的网站提取出来依个爬取
        while self.urls.has_class_url():
            y = y + 1
            print(f"第{y}页")
            print("爬取中")
            print(f"*" * 50)
            try:
                # 获取第一页的网站地址
                new_url = self.urls.get_class_url()
                # 加入头部信息进行请求
                html_content = self.downloader.download(new_url)
                # new_urls, new_data = self.parser.parse(new_url, html_content)
                # 进入解析器进行解析并存入数据库
                new_urls = self.parser.get_new_class(new_url, html_content)
                self.urls.add_new_urls(new_urls)
                # self.outputer.collect_data(new_data,y)

                # exit(0)
            except:
                print("错误")
        print("完成")
            # # 获取详细页面
            # while self.urls.has_new_url():
            #     try:
            #         new_url = self.urls.get_new_url()
            #         print(new_url)
            #         html_content = self.downloader.download(new_url)
            #
            #         # 获取详细界面里的数据
            #         new_data_detail = self.parser.get_new_detail(new_url,html_content)
            #         self.outputer.collect_data_detail(new_data_detail)
            #     # if count == 2:
            #     #     break
            #     # count = count + 1
            #     except:
            #         print('craw failed')

        # self.outputer.output_html()

if __name__ == '__main__':
#     # 开始时间
    start_time = datetime.datetime.now()
#     # 设置爬虫入口
    # conn = sqlite3.connect("分页数据/customers.db")

    root_url = f'https://www.ali213.net/zt/ztisitemap_sale_p1.html'
    obj_spider = Spider_Main()
    obj_spider.craw(root_url)
    # #结束时间
    end_time = datetime.datetime.now()
    print('总用时：%ds'% (end_time - start_time).seconds)
