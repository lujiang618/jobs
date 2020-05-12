import csv
import random
import re
import time
import os
import requests
from pyquery import PyQuery as pq
from requests.exceptions import RequestException

fp = open('Boss直聘.csv', 'wt', newline='', encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('职位', '公司简称', '薪资', '公司地址', '工作经验', '学历', '行业', '融资状况', '公司人数', '联系人', '发布时间', '职位描述+任职资格', '链接'))


def get_one_page(url):
    try:
        print("url:%s"%url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }
        html = requests.get(url, headers=headers)
        if html.status_code == 200:
            return html.text
    except RequestException:
        print('怎么回事要哭了')
        return None


def parse_one_page(html):
    doc = pq(html)
    print("divs")
    print(doc('.job-list'))
    os._exit(1)
    divs = doc('.job-primary')

    for item in divs.items():

        # 招聘职位
        title = item('.job-title').text()
        print(title)
        # 薪资
        salary = item('.red').text()

        awe = item('.info-primary p')
        awe = str(awe)
        result = re.match('^<p>(.*?)<em.*?e"/>(.*?)<em.*?e"/>(.*?)</p>', awe, re.S)

        # 公司地址
        addr = result.group(1)

        # 工作经验
        workEx = result.group(2)

        # 学历
        edu = result.group(3)

        # 公司简称
        company_short_Name = item('.company-text h3').text()

        pfn = item('.info-company .company-text p')
        pfn = str(pfn)
        result = re.match('^<p>(.*?)<em.*?e"/>(.*?)<em.*?e"/>(.*?)</p>', pfn, re.S)

        # 行业
        profess = result.group(1)

        # 融资状况
        finace = result.group(2)

        # 公司人数
        num_person = result.group(3)

        # 联系人
        contacts = item('.info-publis h3').text()

        # 发布时间
        pub_time = item('.info-publis p').text()

        job_url = 'https://www.zhipin.com' + item('.info-primary a').attr('href')

        # 职位描述+任职资格
        detail = get_detail_info(job_url)

        writer.writerow((title, company_short_Name, salary, addr, workEx, edu, detail, profess, finace, num_person, contacts, pub_time, job_url))
        print(title, company_short_Name, salary, addr, workEx, edu, profess, finace, num_person, contacts, pub_time, detail, job_url)

        time.sleep(random.randrange(1, 4))


def get_detail_info(job_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    html_detail = requests.get(job_url, headers=headers).text
    detail_info = pq(html_detail)
    detail = detail_info('.detail-content .job-sec div').text()
    return detail


def main():
    urls = ['https://www.zhipin.com/c101210100/?query=Hadoop&page={0}&ka=page-{1}'.format(i, i) for i in range(1, 30)]
    for url in urls:
        html = get_one_page(url)
        parse_one_page(html)
        os._exit(1)


if __name__ == '__main__':
    main()
