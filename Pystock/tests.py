from django.test import TestCase
import tushare as ts

pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(data.head().to_string())



