# coding: utf-8

import requests
from lxml import etree

from pkg.config import dir_source
from pkg.utils.utils import get_header
from .baseSpider import BaseSpider


class Lagou(BaseSpider):
    website = "拉勾网"
    base_url = "https://www.lagou.com/jobs/positionAjax.json"
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    path = dir_source

    def __init__(self, keyword, city):
        super(Lagou, self).__init__(keyword, city)

    def crawl(self):
        for i in range(1, 31):
            s = requests.get(url="https://www.lagou.com/jobs/list_运维?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=",
                             headers=get_header(), timeout=3)

            cookie = s.cookies

            req = requests.post(self.base_url, headers=self.header, data={'first': True, 'pn': i, 'kd': self.keyword},
                                params={'px': 'default', 'city': self.city, 'needAddtionalResult': 'false'},
                                cookies=cookie, timeout=3)
            text = req.json()

            if "content" not in text.keys():
                print("在第%d页获取不到数据"%i)
                break

            datas = text['content']['positionResult']['result']

            for data in datas:
                s = requests.Session()
                s.get(
                    url='https://www.lagou.com/jobs/list_运维?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
                    headers=get_header(), timeout=3)
                cookie1 = s.cookies
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
