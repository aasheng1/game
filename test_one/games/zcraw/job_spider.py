# -*- coding: utf-8 -*-
# @Author:Thl
# @Time: 2019/8/27
# @Description: 爬取51job信息并存储到mysql中

import requests  # 请求库
from lxml import etree  # 解析html代码
import pymysql  # 连接mysql数据库


def browser(url):
# 伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    # keyword = "python"
    response = requests.get(url=url, headers=headers)  # 请求网址
    response.encoding = "utf-8"
    html = etree.HTML(response.text)  # 实例化
    return html


def get_page_info(url):
    html = browser(url)
    # 游戏详细地址
    type_name = html.xpath('//ul[@class="list"]/li/span')
    for type in type_name:
        print(type.xpath('./text()')[0])
    po_min = []
    po_max = []
    mins = html.xpath('//div[@class="small_list"]/ul/li')
    for min in mins:
        po_min.append(min.xpath('./img/@src')[0])
    print(po_min)
    maxs = html.xpath('//div[@class="large_box"]/ul/li')
    for max in maxs:
        po_max.append(max.xpath('./img/@src')[0])
    print(po_max)
    #     job_name = job.xpath('./p/span/a/@title')[0]
    #     com_name = job.xpath('./span[@class="t2"]/a/@title')[0]
    #     cominfo_url = job.xpath('./span[@class="t2"]/a/@href')[0]
    #     address = job.xpath('./span[@class="t3"]/text()')[0]
    #     salary = job.xpath('./span[@class="t4"]/text()')
    #     if salary:  # 有的没有公布薪资，所以取不到值
    #         salary = salary[0]
    #     else:
    #         salary = ''
    #     release_time = job.xpath('./span[@class="t5"]/text()')[0]
    #     # db.insert_data(job_name, jobinfo_url, com_name, cominfo_url, address, salary, release_time)  # 调用数据库插入函数
    # next_page_url = html.xpath('//li[@class="bk"][2]/a/@href')
    # if next_page_url:
    #     next_page_url = next_page_url[0]
    # else:
    #     print("已经是最后一页了。")
    #     return
    # print("下一页地址为:  ", next_page_url)
    # get_page_info(next_page_url, headers)


class InsertDb(object):
    def __init__(self):  # 初始化
        # 连接数据库                 地址        用户名  密码      数据库     指定字符集
        self.db = pymysql.connect("192.168.0.215","califeng","Sanchuang1234#", "sanchuang", charset="utf8")
        self.cursor = self.db.cursor()  # 创建游标
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_info(
            id INT PRIMARY KEY AUTO_INCREMENT,
            job_name VARCHAR(50), 
            jobinfo_url VARCHAR(100),
            com_name VARCHAR(50),
            com_url VARCHAR(100),
            address VARCHAR(20),
            salary VARCHAR(20),
            release_time VARCHAR(10))
        """)  # 执行sql语句，创建数据表
        self.db.commit()  # 提交到数据库

    def insert_data(self, *data):
        sql = f"INSERT INTO job_info(job_name,jobinfo_url,com_name,com_url,address,salary,release_time) VALUES {data}"
        try:
            self.cursor.execute(sql)  # 执行插入语句
            self.db.commit()  # 提交到数据库
            print(f"{data}数据保存成功！")
        except Exception as e:
            print(e)
            self.db.rollback()  # 数据库回滚

    def close_connect(self):  # 与数据库断开连接
        self.cursor.close()
        self.db.close()

def game_details(url):
    html = browser(url)
    download_url = html.xpath('//*[@id="goxlbtn"]')
    return download_url

# db = InsertDb()  # 连接数据库并初始化
# get_page_info(url, headers, db)
url = 'https://dl.3dmgame.com/pc/99044.html'
get_page_info(url)
# db.close_connect()  # 关闭数据库连接



