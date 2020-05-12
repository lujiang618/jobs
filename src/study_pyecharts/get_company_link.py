from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os


def request(browser, url):
    browser.get(url)
    timeout = WebDriverWait(browser, 1)
    while True:
        js_down = "var q=document.documentElement.scrollTop=1100"
        js_down1 = "var q=document.documentElement.scrollTop=1800"
        browser.execute_script(js_down)
        time.sleep(0.5)
        browser.execute_script(js_down1)
        time.sleep(0.5)
        link = browser.find_elements_by_css_selector('.sub-li a:nth-of-type(1)')
        name = browser.find_elements_by_css_selector('.conpany-text h4')
        for i, j in zip(link, name):
            'https://www.zhipin.com/gongsir/131981ab87757a001nxy0tW9Fg~~.html'
            data = {
                '公司名': j.text,
                '超链接': str(i.get_attribute('href')).replace('gongsi',
                                                            'gongsir') + '?city=101280600&ka=sel_city_101280600'
            }
            print(data)
            with open('company_link.txt', 'a+', encoding='utf-8') as A:
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
    url = 'https://www.zhipin.com/gongsi/?ka=header_brand'
    request(browser, url)


if __name__ == '__main__':
    main()
