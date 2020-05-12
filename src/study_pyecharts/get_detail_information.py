from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import pandas


def request(browser):
    link = pandas.read_excel(r'C:\Users\14455\Desktop\BOSS直聘职位信息.xlsx', sheet_name='Sheet1')
    with open('BOSS_result2020-03-21.txt','r',encoding='utf-8')as R:
        save_ed = R.read()
        R.close()
    for i, j in zip(link['超链接'], link['发布时间']):
        if str(i) in save_ed:
            continue
        browser.get(i)
        try:
            js_down = "var q=document.documentElement.scrollTop=1100"
            js_down1 = "var q=document.documentElement.scrollTop=1800"
            time.sleep(0.5)
            browser.execute_script(js_down)
            time.sleep(0.5)
            browser.execute_script(js_down1)
            company = browser.find_element_by_css_selector('.job-sec .name').text
            job_name = browser.find_element_by_css_selector('.info-primary .name h1').text
            adress = browser.find_element_by_css_selector('.location-address').text
            price = browser.find_element_by_css_selector('span.badge').text
            soup = BeautifulSoup(browser.page_source, 'lxml')
            educational = soup.select('div > div > div.info-primary > p')
            data = {
                '公司名称': company,
                '职位名称': job_name,
                '详情链接': i,
                '公司地址': adress,
                '薪资待遇': price,
                '要求学历': list(educational[0].strings)[-1],
                '发布时间': j
            }
            print(data)
            with open('BOSS_result{}.txt'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))), 'a+',
                      encoding='utf-8')as A:
                A.write(str(data) + '\n')
                A.close()
        except:
            continue

def main():
    os.system("taskkill /f /im chromedriver.exe")
    browser = webdriver.Chrome()
    request(browser)



if __name__ == '__main__':
    main()
