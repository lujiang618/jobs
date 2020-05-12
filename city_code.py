# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pkg.config import dir_areas

if __name__ == '__main__':
    result = requests.get('http://www.mca.gov.cn/article/sj/xzqh/2020/2020/202003301019.html')

    bs = BeautifulSoup(result.text, "html.parser")

    city = []
    province = []
    areas = []
    current_province = ""
    current_city = ""
    for tr in bs.find_all(name="tr"):
        area = {}
        area_type = ''
        for td in tr.find_all(name="td"):
            # 省和市
            if td.get("class") and td['class'][0] == "xl7030721":
                # print(td.get_text())
                if td.get_text().isdigit():
                    area['code'] = td.get_text().strip()
                else:
                    area['name'] = td.get_text().strip()
                # 市
                if td.find(name="span") and not td.get_text().isdigit():
                    area_type = "city"
                else:
                    area_type = "province"

            if td.get("class") and td['class'][0] == "xl7130721":
                area_type = "area"
                if td.get_text().isdigit():
                    area['code'] = td.get_text().strip()
                else:
                    area['name'] = td.get_text().strip()

        if area_type == "city":
            area['province'] = current_province
            city.append(area)
            current_city = area['code']
        elif area_type == "province":
            province.append(area)
            current_province = area['code']
            if area['code'] in ['110000', '310000', '120000', '500000']:
                area['province'] = current_province
                city.append(area)
        elif area_type == "area":
            area['city'] = current_city if current_city else current_province
            areas.append(area)

    print("数据获取完成，开始保存")
    province = pd.DataFrame(province)
    province.to_csv(dir_areas+"province.csv", encoding='utf_8_sig', index=False)
    city = pd.DataFrame(city)
    city.to_csv(dir_areas+"city.csv", encoding='utf_8_sig', index=False)
    areas = pd.DataFrame(areas)
    areas.to_csv(dir_areas+"areas.csv", encoding='utf_8_sig', index=False)
