# -*- coding: utf-8 -*-
"""
从163网址上获取指定ID指定时间段的K线数据，入库
"""
import pandas as pd
import tushare as ts
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
import Data.data as dt

def init_mysql():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(BASE_DIR)
    SQL_DIR = BASE_DIR + r'\Mysql'
    sql = mysql.sql()
    sql.init_by_cfg_file(SQL_DIR + r'\sql_config.json')
    return sql


if __name__ == '__main__':
    # initial database
    myinit = init_mysql()

    data = dt.data()

    # 获取盈利能力数据
    for yea in range(2018,2019):
        for qua in range(1,5):
            try:
                print(yea,qua)
                reportDB = data.get_profit_data(yea,qua)
                reportDB["year"] = yea
                reportDB["quarter"] = qua
                reportDB = reportDB['year', 'quarter', 'code', 'name', 'roe', 'net_profit_ratio', 'gross_profit_rate',
                'net_profits', 'eps', 'business_income', 'bips']
                print(reportDB.head())
                myinit.df_to_mysql("profit_data", reportDB)
            except Exception as e:
                print(e)
                print("获取盈利能力数据失败！")
                continue