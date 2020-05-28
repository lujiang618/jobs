# coding: utf-8

import random
import time

import requests
from lxml import etree

from pkg.config import dir_source
from pkg.utils.utils import get_header
from .baseSpider import BaseSpider


class LaGou(BaseSpider):
    website = "拉勾网"
    base_url = "https://www.lagou.com/jobs/positionAjax.json"
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    path = dir_source

    cookie_url = "https://www.lagou.com/jobs/list_运维?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput="

    def __init__(self, keyword, city):
        super(LaGou, self).__init__(keyword, city)

    def crawl(self):
        for i in range(1, 31):
            print("开始获取第%d页数据" % i)

            text = self.get_list(i)
            if "content" not in text.keys():
                print("在第%d页获取不到数据，result:%s" % (i, text))
                break

            datas = text['content']['positionResult']['result']
            for data in datas:
                self.get_detail(data)

            s_time = self.get_random_number()
            print("获取第%d页数据成功, sleep %s 秒" % (i, s_time))
            time.sleep(s_time)

    def get_list(self, i):
        cookie = self.get_cookies()
        post_params = {'first': True, 'pn': i, 'kd': self.keyword}
        get_params = {'px': 'default', 'city': self.city, 'needAddtionalResult': 'false'}
        req = requests.post(self.base_url, headers=self.header, data=post_params, params=get_params, cookies=cookie, timeout=3)
        text = req.json()

        s_time = self.get_random_number()
        print("获取第%d页列表数据成功, sleep %s 秒" % (i, s_time))
        time.sleep(s_time)

        return text

    def get_random_number(self):
        number = random.randint(5, 10)
        return number

    def get_cookies(self):
        s = requests.get(url=self.cookie_url, headers=get_header(), timeout=3)
        cookie = s.cookies

        s_time = self.get_random_number()
        print("获取cookie后, sleep %s 秒" % s_time)
        time.sleep(s_time)

        return cookie

    def get_detail(self, data):
        # s = requests.Session()
        # s.get(url=self.cookie_url, headers=get_header(), timeout=3)
        # cookie1 = s.cookies

        cookie1 = self.get_cookies()
        url = 'https://www.lagou.com/jobs/' + str(data.get('positionId')) + '.html'
        req1 = requests.get(url, headers=self.header, cookies=cookie1)
        req1.encoding = 'utf-8'
        html = etree.HTML(req1.text)
        detail = ''.join(html.xpath('//*[@class="job-detail"]//*/text()')).strip()
        if detail.isspace():
            detail = ''.join(html.xpath('//*[@class="job-detail"]/text()')).strip()
        data = {
            "职位名称": data.get('positionName'),
            "工作地点": data.get('district'),
            "薪资": data.get('salary'),
            "公司名称": data.get('companyFullName'),
            "经验要求": data.get('workYear'),
            "学历": data.get('education'),
            "福利": data.get('positionAdvantage'),
            "详细链接": url,
            "职位信息": detail
        }
        self.data.put(data)

        s_time = self.get_random_number()
        print("获取%s-%s招聘信息后, sleep %s 秒" % (data['公司名称'], data['职位名称'], s_time))
        time.sleep(s_time)
