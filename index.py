# coding: utf-8

import os

from src.spiders.lagou import Lagou

if __name__ == '__main__':
    city = input('请输入城市名：')
    keyword = input('请输入搜索关键词：')
    if keyword != None and city != None:
        Lagou(city=city, keyword=keyword).run()
