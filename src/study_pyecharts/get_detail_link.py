from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os


def request(browser, timeout, url, company):
    browser.get(url)
    while True:
        js_down = "var q=document.documentElement.scrollTop=1100"
        js_down1 = "var q=document.documentElement.scrollTop=1800"
        js_down2 = "var q=document.documentElement.scrollTop=2400"
        js_down3 = "var q=document.documentElement.scrollTop=3000"
        js_down4 = "var q=document.documentElement.scrollTop=3600"
        browser.execute_script(js_down)
        time.sleep(0.5)
        browser.execute_script(js_down1)
        time.sleep(0.5)
        browser.execute_script(js_down2)
        time.sleep(0.5)
        browser.execute_script(js_down3)
        time.sleep(0.5)
        browser.execute_script(js_down4)
        job_detail_link = browser.find_elements_by_css_selector('div.job-list > ul > li > a')
        creat_time = browser.find_elements_by_css_selector('.job-pub-time')
        for i, j in zip(job_detail_link, creat_time):
            data = {
                '公司名称': company,
                '超链接': i.get_attribute('href'),
                '发布时间': j.text
            }
            print(data)
            with open('job_detail_link.txt', 'a+', encoding='utf-8')as A:
                A.write(str(data) + '\n')
                A.close()
        try:
            timeout.until(EC.element_to_be_clickable((By.CLASS_NAME, 'disabled')))
            break
        except:
            pass
        try:
            next_page = timeout.until(EC.element_to_be_clickable((By.CLASS_NAME, 'next')))
            next_page.click()
        except:
            break


def main():
    os.system("taskkill /f /im chromedriver.exe")
    browser = webdriver.Chrome()
    browser.get('https://login.zhipin.com/?ka=header-login')
    timeout = WebDriverWait(browser, 300)
    timeout.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                    '#container > div.user-jobs-area > div > div.condition-box > div.filter-select-box > span'),
                                                   '清空筛选条件'))
    timeout2 = WebDriverWait(browser, 1)
    with open('company_link.txt', 'r', encoding='utf-8')as R:
        for i in R.readlines():
            if eval(i)['公司名'] == '腾讯':
                continue
            request(browser, timeout2, eval(i)['超链接'], eval(i)['公司名'])
        R.close()


if __name__ == '__main__':
    main()
