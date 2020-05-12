# coding: utf-8

import random
import time

import requests
from lxml import etree

from pkg.config import dir_source
from pkg.utils.utils import get_header
from .baseSpider import BaseSpider


class ZhiLian(BaseSpider):
    website = "智联招聘"

    base_url = ""
    header = {

    }

    path = dir_source

    def __init__(self, keyword, city):
        super(ZhiLian, self).__init__(keyword, city)


    def crawl(self):
        pass
