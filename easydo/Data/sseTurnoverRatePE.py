# -*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import pandas as pd
import sys

currentPath = os.path.dirname(os.path.abspath(__file__))
chromeD = currentPath + os.path.sep + "src" + os.path.sep + "chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('log-level=3')
browser = webdriver.Chrome(
    chrome_options=chrome_options, executable_path=chromeD)

browser.implicitly_wait(3)
browser.get("http://www.sse.com.cn/market/stockdata/overview/day/")

elem0 = browser.find_element_by_xpath(
    "//*[@id='tableData_934']/div[2]/table/tbody/tr[8]/td[2]/div").text
elem1 = browser.find_element_by_xpath(
    "//*[@id='tableData_934']/div[2]/table/tbody/tr[8]/td[3]/div").text
elem2 = browser.find_element_by_xpath(
    "//*[@id='tableData_934']/div[2]/table/tbody/tr[8]/td[4]/div").text

elem3 = browser.find_element_by_xpath(
    '//*[@id="tableData_934"]/div[2]/table/tbody/tr[7]/td[2]/div').text
elem4 = browser.find_element_by_xpath(
    '//*[@id="tableData_934"]/div[2]/table/tbody/tr[7]/td[3]/div').text
elem5 = browser.find_element_by_xpath(
    '//*[@id="tableData_934"]/div[2]/table/tbody/tr[7]/td[4]/div').text

curTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
print("{} {}".format(browser.title, curTime))
print("上海市場 换手率(%) {}".format(elem0))
print("A股 换手率(%) {}".format(elem1))
print("B股 换手率(%) {}".format(elem2))
print("上海市場 平均市盈率 {}".format(elem3))
print("A股 平均市盈率 {}".format(elem4))
print("B股 平均市盈率 {}".format(elem5))
browser.quit()

parentPath = os.path.dirname(currentPath) + os.path.sep + "Mysql"
print(parentPath)

sys.path.append(parentPath)
import mysql

dataL = []
shanghaiL = []
AL = []
BL = []
shanghaiL2 = []
AL2 = []
BL2 = []
dataL.append(curTime)
shanghaiL.append(elem0)
AL.append(elem1)
BL.append(elem2)
shanghaiL2.append(elem3)
AL2.append(elem4)
BL2.append(elem5)
df = pd.DataFrame({
    "Date": dataL,
    "SHTurnOver": shanghaiL,
    "ATurnOver": AL,
    "BTurnOver": BL,
    "SHPE": shanghaiL2,
    "APE": AL2,
    "BPE": BL2
})

df = df[["Date", "SHTurnOver", "ATurnOver", "BTurnOver", "SHPE", "APE", "BPE"]]
print(df)
# 初始化入庫模塊并數據入庫
inmysql = mysql.sql()
inmysql.init_by_cfg_file(parentPath + os.path.sep + 'sql_config.json')
inmysql.df_to_mysql("sseTurnOverRatePE", df)
print("完成數據入庫mysql")