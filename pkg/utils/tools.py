# coding: utf-8

import csv
import datetime
import logging
import os
import shutil

import matplotlib.pyplot as plt


# 删除data目录下所有文件
def del_data_file(data_path):
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    file_list = os.listdir(data_path)

    for file in file_list:
        file_path = os.path.join(data_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path, True)


def save2csv(column, rows, file):
    fp = open(file, 'w', encoding='utf-8', newline='')
    file = csv.writer(fp, quoting=csv.QUOTE_ALL, doublequote=True, escapechar='')
    file.writerow(column)
    file.writerows(rows)
    fp.close()


def paint_common(title, path, x_label='Date'):
    plt.gcf().autofmt_xdate(rotation=50)
    plt.axis('tight')
    plt.xlabel(x_label, size=20)

    plt.title(title, size=20)
    plt.tick_params(axis='x', labelsize=9)  # 设置x轴标签大小
    plt.legend(loc='best')

    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(path + title + '.png')

    plt.show()


def print_star(text):
    print("*" * 60 + text + "*" * 60)


def path_exists(path_list):
    for path in path_list:
        if os.path.exists(path):
            continue
        os.makedirs(path)


# log数据时效要求并不是很高，可以改成异步操作
def write_log(dir_logs, file_name, data):
    today = datetime.date.today()
    dir_path = dir_logs + today.strftime('%Y-%m-%d') + '/'

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    log_file = dir_path + file_name
    handler = logging.FileHandler(log_file)

    formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info(data)
    logger.removeHandler(handler)  # 有多个handler时会同时向这几个文件写数据
