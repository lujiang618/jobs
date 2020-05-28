# coding: utf-8

import random
import time

import requests
from lxml import etree

from pkg.config import dir_source
from pkg.utils.utils import get_header
from .baseSpider import BaseSpider


class Boss(BaseSpider):
    website = "Boss直聘"

    base_url = ""
    header = {

    }

    path = dir_source

    def __init__(self, keyword, city):
        super(Boss, self).__init__(keyword, city)


    def crawl(self):
        pass
