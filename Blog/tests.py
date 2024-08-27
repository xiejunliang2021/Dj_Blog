from django.test import TestCase
import pandas as pd
import tushare as ts


pro = ts.pro_api()
df_limit = pro.stk_limit(trade_date='20240827')
# print(df_limit)

df_code = pro.daily(trade_date='20240827')
merged_df = pd.merge(df_code, df_limit, on=['trade_date', 'ts_code'])
print(merged_df.head().to_string())

