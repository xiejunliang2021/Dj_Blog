


from django.test import TestCase
import tushare as ts

import os
import django

# 设置 DJANGO_SETTINGS_MODULE 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dj_Blog.settings')

# 初始化 Django 环境
django.setup()
from Pystock.models import StockCode
import pandas as pd


pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,market,list_status,is_hs')
data['list_date'] = pd.to_datetime(data['list_date'], format='%Y%m%d')
print(data.head().to_string())
# print(data.ts_code)

stock = [
    StockCode(
        ts_code=row[0],
        symbol=row[1],
        name=row[2],
        area=row[3],
        industry=row[4],
        market=row[5],
        list_status=row[6],
        list_date=row[7],
        is_hs=row[8]
        )
    for row in data
]
print('------------------------------------------------')
print(stock)






