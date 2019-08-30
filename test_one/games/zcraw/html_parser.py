# coding = utf-8
import re
import urllib
from urllib.parse import urlparse
from zcraw import html_downloader
from bs4 import BeautifulSoup
import sqlite3
import django
import os
from apps.download.models import GameDetails,GameClass,Publishers
from selenium import webdriver
from selenium.webdriver import ActionChains



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "games.settings")  # website可以更改为自己的项目名称
django.setup()  # Django版本大于1.7 加入这行代码

class HtmlParser(object):
    def __init__(self):
        #设置HTML下载器
        self.downloader = html_downloader.HtmlDownloader()

    def get_new_class(self, page_url, html_content):
        if page_url is None or html_content is None:
            return None
        soup = BeautifulSoup(html_content, 'html.parser', )
        new_urls = list()
        # res_data = {}
        #/view/123.htm
        # links = soup.find_all('a', href=re.compile(r'/item/.*?'))
        # links = soup.select('div.list-con-main.clearfix li.list-con-main-item.normal .item-btn a')[::3]

        # 获取到这一页所有需要爬取详细信息的链接
        links = soup.select('div.list-con-main.clearfix li.list-con-main-item.normal')
        # 进行for循环依个爬取
        for link in links:
            try:
                minute = list()
                soup_data = BeautifulSoup(str(link), 'html.parser')
                soup_data.prettify()
                down_link = soup_data.select('.item-btn a')[0]
                # 获取“点击下载”的链接
                new_url = down_link['href']
                new_full_url = urllib.parse.urljoin(page_url, new_url)
                new_urls.append(new_full_url)
                # 获取游戏的名字
                name1 = soup_data.select('a')[1].get_text()
                print(name1)
                # 获取到游戏的评分
                grade = soup_data.select('a span')[0].get_text()
                print(grade)
                # 获取到游戏的海报
                tupian = soup_data.select('a img')[0]['src']
                print(tupian)


                if not GameDetails.objects.filter(game_name=name1):
                    print(f"爬取《{name1}》的详细信息")
                    print("=" * 50)
                    # 进入“点击下载”的链接再次爬取
                    html_enter = self.downloader.download(new_full_url)
                    # 将得到的文本传入爬取游戏详情函数
                    res_data_detail = self.get_new_detail(new_full_url,html_enter)
                    # 将数据存入列表，再将列表存入Value值
                    minute.append(name1)
                    minute.append(new_full_url)  # 存入游戏主页
                    minute.append(grade)
                    minute.append(tupian)
                    # res_data[name1] = minute


                    type = res_data_detail[0]
                    time = res_data_detail[1]
                    label = res_data_detail[2]
                    publisher = res_data_detail[3]
                    size = res_data_detail[4]
                    suffix = res_data_detail[5]
                    screen = res_data_detail[6]
                    screen_min_list = res_data_detail[7]
                    introduce = res_data_detail[8]
                    BT_link = res_data_detail[9]
                    game_link = res_data_detail[10]
                    baiduyun = res_data_detail[11]



                    # c.execute("INSERT INTO GamesDetails VALUES (?,?,?)",

                    # GameDetails.objects.create(game_name=name1)
                    # GameDetails.objects.create(down_url=new_full_url)
                    # GameDetails.objects.create(grade=grade)
                    # GameDetails.objects.create(poster=tupian)

                    # 将没有下载地址的游戏筛选出去
                    # 并存入数据库
                    if new_url != 'javascript:void(0)':
                        print(f"存储数据中...")
                        if not Publishers.objects.filter(publistshers_name=publisher):
                            Publishers.objects.create(publistshers_name=publisher)
                        if not GameClass.objects.filter(type_name=type):
                            GameClass.objects.create(type_name=type)
                        type_id = GameClass.objects.get(type_name=type)
                        type_id_new = type_id.id
                        publisher_id = Publishers.objects.get(publistshers_name=publisher)
                        publisher_id_new = publisher_id.id

                        GameDetails.objects.create(
                            game_name=name1, down_url=new_full_url, grade=grade, poster=tupian,
                            sell=time,tag=label,size=size,name_alias=suffix,picture_max=screen,publishers_id=publisher_id_new,gameclass_id=type_id_new,picture_min=screen_min_list,
                            introduce=introduce,BT_link=BT_link,game_link=game_link,baiduyun=baiduyun,
                        )

                        print(f"存储成功")
                    else:
                        print("没有下载地址")
                    print("")
                        # print("")
                else:
                    print("已存在，跳过")
            except Exception as ex:
                print("报错了")
        # conn.commit()
        # conn.close()
        return new_urls

    #获取标题、摘要
    def get_new_detail(self, page_url,html_content):
        if page_url is None or page_url == 'javascript:void(0)' or html_content is None:
            return None
        soup = BeautifulSoup(html_content, 'html.parser',)
        # 新建字典
        res_data_detail = list()
        try:
            type = soup.select('div.detail_game_l_r_info.mt5 li a')[0].get_text()
            res_data_detail.append(type)
            # print(type)

            # 游戏发售时间
            time = soup.select('div.detail_game_l_r_info.mt5 li a')[1].get_text()
            res_data_detail.append(time)
            # print(time)

            # 游戏标签
            label_list = []
            label = soup.select('.detail_game_l_r_tag a')
            for i in label:
                label_list.append(i.get_text())
                # print(i.get_text(), end=' ')
            res_data_detail.append(label_list)

            # 游戏发行商
            publisher = soup.select('div.detail_game_l_r_info.mt5 li')[2].get_text()[5::]
            res_data_detail.append(publisher)
            # print(publisher)

            # 游戏大小
            size = soup.select('.detail_game_l_r_down_l font')[0].get_text()[5::]
            res_data_detail.append(size)
            # print(size)

            # 游戏价格
            # price = soup.select('div.detail_body_left_xgxx_b span')[2].get_text()
            # print(price)

            # 游戏完整下载名
            suffix = soup.select('.detail_game_l_r_etit span')[0].get_text()
            res_data_detail.append(suffix)
            # print(suffix)

            # 游戏截图(大图)
            screen_list = []
            screen = soup.select('.detail_body_con_jt_con_img img')
            # print("游戏截图大图")
            for i in screen:
                screen_list.append(f"https:{i['src']}")
                # print(f"https:{i['src']}")
            res_data_detail.append(screen_list)
            # print(printscreen)

            # 游戏截图（小图）
            screen_min_list = []
            screen_min = soup.select('.detail_body_con_bb_con_bottom_center img')
            # print("游戏截图小图")
            for i in screen_min:
                screen_min_list.append(f"https:{i['src']}")
                # print(f"https:{i['src']}")
            res_data_detail.append(screen_min_list)

            # 游戏介绍
            introduce = soup.select('.detail_body_left_info_con')[0].get_text()
            res_data_detail.append(introduce)
            # print(introduce)

            # 安装说明
            # explain = soup.select('.detail_body_left_info_con p')[1].get_text()
            # print(f"安装说明{explain}")
            response = self.downloader.down_link(page_url)
            soup_url = BeautifulSoup(response.text, "html.parser")
            # print(soup_url)

            # 进入要下载的BT种子页面
            try:
                down_link = soup_url.select('.result_xl')[0]['href']

                # print(f"BT种子链接：{down_link}")
                down_html = self.downloader.download(down_link)
                soup_finally = BeautifulSoup(down_html,'html.parser')
                BT_link = soup_finally.select("#btbtn")[0]['href']
                game_link = soup_finally.select("a.gameDown.down_xl")[0]["href"]
                baiduyun = soup_finally.select("#wpbtn")[0]["href"]
                # print(f"BT种子：{BT_link}")
                res_data_detail.append(BT_link)

                # print(f"迅雷下载：{game_link}")
                res_data_detail.append(game_link)

                # print(f"百度网盘：{baiduyun}")
                res_data_detail.append(baiduyun)

                print("=" * 50)
            except:
                print("BT种子爬取失败")
            # print(res_data_detail)
            return res_data_detail
        except:
            print("没有下载地址")

    # def parse(self, page_url, ):
    #     new_urls = self._get_new_urls(page_url, soup)
    #     new_data = self._get_new_data(page_url, soup)
    #     return new_urls, new_data
    #
    # def get_downlink(self, page_url, html_content):
    #     if page_url is None or html_content is None:
    #         return None
    #     soup = BeautifulSoup(html_content, 'html.parser', )
    #     down_bt =

