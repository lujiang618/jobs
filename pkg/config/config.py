# coding: utf-8

import os
import sys

import yaml

from pkg.utils.tools import path_exists


# 获取配置
def get_config():
    config_dict = {}

    if not os.path.exists(config_file):
        return config_dict

    with open(config_file, 'rb') as f:
        config_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    return config_dict


product_name = 'jobs'
root_start = sys.path[0].index(product_name)
root_end = root_start + len(product_name)

# 根目录
root_dir = sys.path[0][0:root_end]

# 配置文件路径
config_file = root_dir + '/config/config.yaml'
if os.path.exists(root_dir + '/config/config.local.yaml'):
    config_file = root_dir + '/config/config.local.yaml'

dir_data = root_dir + '/data/'  # data 目录
dir_areas = dir_data + '/areas/'  # data 目录
dir_source = dir_data + 'source-data'  # data 目录


data_path_list = [
    dir_data,
    dir_areas,
    dir_source,
]

path_exists(data_path_list)
config = get_config()
