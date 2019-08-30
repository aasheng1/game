import urllib
import urllib.request
import random
import os
import django
from selenium.webdriver import ActionChains
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "games.settings")#website可以更改为自己的项目名称
django.setup()#Django版本大于1.7 加入这行代码

class HtmlDownloader(object):

    def download(self, url):
        if url is None or url == 'javascript:void(0)':
            return None

        #伪装成浏览器访问，直接访问的话csdn会拒绝
        user_agent = random.choice([
            'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            # 搜狗浏览器
            'Mozilla / 4.0(compatible;MSIE7.0;WindowsNT5.1;Trident / 4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
            # 360浏览器
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; 360SE))'
            # Chrome浏览器
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            ])
        # user_agent = random.choice(user_list)
        headers = {'User-Agent':user_agent}

        # 伪装代理池
        proxies = {
            'http': 'https://120.83.99.240:9999'
        }
        #构造请求
        response = requests.get(url,headers=headers).content
        # response = requests.get(url,headers=headers,proxies=proxies).content
        # response.encoding = 'utf-8'
        # print(response)

        #访问页面
        # response = urllib.request.urlopen(req)
        #python3中urllib.read返回的是bytes对象，不是string,得把它转换成string对象，用bytes.decode方法
        return response


    def down_link(self,url):

        # 代理IP池
        # PROXY = [
        #     "120.83.99.240:9999",
        # ]
        # chromeOptions = webdriver.ChromeOptions()
        # chromeOptions 是一个配置 chrome 启动时属性的类。
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument(f'--proxy-server={PROXY}')

        # 浏览器不提供可视化页面.
        #linux下如果系统不支持可视化不加这条会启动失败
        chrome_options.add_argument('--headless')

        # 禁止图片加载
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)

        browser = webdriver.Chrome()
        # browser = webdriver.Chrome(chrome_options = chromeOptions)
        browser.get(url)
        input_str = browser.find_element_by_id('game591BoxOpen')
        input_str.click()
        # html = dri
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.select(".pageCont")
        # print(div)
        response = requests.get("https:" + div[0]["src"])
        browser.close()
        return response

