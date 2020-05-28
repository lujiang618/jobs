# coding: utf-8

import os

from src.spiders.lagou import LaGou

if __name__ == '__main__':
    city = '上海'
    keyword = '财务'
    LaGou(city=city, keyword=keyword).run()

