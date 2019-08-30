'''
filename = craw.py
author = LJH
date = 2019/08/28
'''

from selenium import webdriver
from lxml import etree
import time,os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "summer_project.settings")
django.setup()

driver = webdriver.Chrome()
driver.get("https://so.iqiyi.com/so/q_%E8%8B%B1%E6%96%87%E7%94%B5%E5%BD%B1%20%E7%88%B1%E6%83%85?source=input&sr=885530010954")


def get_info():
    html = driver.page_source  # 获取当前网页源代码
    html = etree.HTML(html)  # 实例化
    li_list = html.xpath('/html/body/div[1]/div[4]/div[1]/div/div[2]/div/ul/li[1]/div/div/div[3]/div/ul/li')
    for li in li_list:
        movie_name = li.xpath('./div[1]/a/@title')[0]
        img_url = 'https:' + li.xpath('./div[1]/a/img/@src')[0]
        actor_list = li.xpath('./div[2]/p[2]/a/text()')
        actors = ' '.join(actor_list)
        url = li.xpath('./div[1]/a/@href')[0]
        Movie.objects.create(movie_name=movie_name,movie_actor=actors,movie_picture=img_url,movie_source=url)
        print(f"电影名： {movie_name}   图片地址：  {img_url}   演员： {actors}   链接：  {url}")

get_info()  # 第一次获取信息

for i in range(4):
    time.sleep(0.5)
    driver.find_element_by_xpath('//a[@data-pager-elem="next"]').click()
    get_info()