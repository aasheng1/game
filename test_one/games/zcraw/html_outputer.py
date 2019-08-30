import xlwt
import os
import json
import sqlite3
class HtmlOutputer(object):

    def __init__(self):
        self.datas = []
        self.datas_detail = []

    def collect_data(self, data, y):
        if data is None:
            return
        # self.datas.append(data)
        self.save(data, y)


    def collect_data_detail(self, data_detail):
        if data_detail is None:
            return
        self.datas_detail.append(data_detail)


    def output_html(self):
        # 创建workbook
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建工作表
        mysheet = workbook.add_sheet('中彩网福彩3D开奖数据', cell_overwrite_ok=True)

    # 存储数据
    def save(self, data, i):

        print("*" * 200)
        if not os.path.exists("分页数据"):
            os.mkdir("分页数据")
        os.chdir("./分页数据")
        print("准备存储数据")
        with open(f"第{i}页数据.txt", "w+", encoding="utf-8") as f:
            f.write(json.dumps(data))
            # content = json.loads(f.read())
        print("数据存储完毕")
        os.chdir("../")