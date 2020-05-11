# coding: utf-8

import csv
import os
import queue


class BaseSpider(object):
    keyword = ""
    city = ""

    csv_header = ['职位名称', '详细链接', '工作地点', '薪资', '公司名称', '经验要求', '学历', '福利', '职位信息']

    website = ""
    base_url = ""
    header = {}

    data = queue.Queue()

    path = ""

    def __init__(self, keyword, city):
        self.keyword = keyword
        self.city = city

    def crawl(self):
        pass

    def run(self):
        self.crawl()

        if os.path.exists(self.path):
            data_list = []
            while not self.data.empty():
                data_list.append(self.data.get())

            file = os.path.join(self.path, '{}_关键词_{}_城市_{}.csv'.format(self.website, self.keyword, self.city))
            with open(file, 'w', newline='', encoding='utf-8-sig') as f:
                f_csv = csv.DictWriter(f, self.csv_header)
                f_csv.writeheader()
                f_csv.writerows(data_list)
