# -*- coding: utf-8 -*-
"""
从163网址上获取指定ID指定时间段的K线数据，入库
"""
import requests
import re
import datetime
import pandas as pd
import mysql
import os
import sys

# 导入自定义模块
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import Data.get_price as get_price

def init_mysql():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(BASE_DIR)
    SQL_DIR = BASE_DIR + r'\Mysql'
    sql = mysql.sql()
    sql.init_by_cfg_file(SQL_DIR + r'\sql_config.json')
    return sql


if __name__ == '__main__':
    print(sys.path)

    # initial database
    myinit = init_mysql()

    # K线数据入库
    start_day = '20100625'
    company_list = ['600660', '600066', '000651', '600522', '601012', '600887']
    for id in company_list:
        s = get_price.get_period_k_day(id,start_day)
        print("正在入库{} K线数据".format(id))
        myinit.df_to_mysql("K_day", s)
        print("{} K线数据入库完成".format(id))
