from django.test import TestCase
import pandas as pd
import tushare as ts


pro = ts.pro_api()
df = pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')
print(df.head().to_string())

df_01 = pro.query('trade_cal', start_date='20180101', end_date='20181231')
print(df_01)

