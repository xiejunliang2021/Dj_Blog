# def add_history_price(request):
#     if request.method == "GET":
#         return render(request, 'add_history_price.html')
#
#     pro = ts.pro_api()
#     # 从页面获取post传递过来的数据
#     trade_date = request.POST.get('trade_date')
#     # 从数据库中获取对应的数据
#     date_is_open = TradeIsOpen.objects.filter(cal_date=trade_date)
#     print(date_is_open)
#     # 判断今天是否开盘
#     if date_is_open.cal_date == '0':
#         return HttpResponse('今天不开盘')
#     df_limit = pro.stk_limit(trade_date=trade_date)
#     df_price = pro.daily(trade_date=trade_date, fields='ts_code,trade_date, open, close, high, low, '
#                                                        'pre_close, change, pct_chg, vol, amount')
#     df = pd.merge(df_price, df_limit, on=['trade_date', 'ts_code'])
#     df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
#
#     # 假设需要插入的 ts_code 已经在数据库中
#     code_info_dict = {code.ts_code: code for code in CodeInfo.objects.all()}
#
#     # 准备插入的数据
#     records = []
#     for _, row in df.iterrows():
#         ts_code = row['ts_code']
#         if ts_code in code_info_dict:
#             records.append({
#                 'ts_code': code_info_dict[ts_code].ts_code,  # 使用正确的字段名
#                 'trade_date': row['trade_date'],
#                 'open': row['open'],
#                 'close': row['close'],
#                 'high': row['high'],
#                 'low': row['low'],
#                 'pre_close': row['pre_close'],
#                 'change': row['change'],
#                 'pct_chg': row['pct_chg'],
#                 'vol': row['vol'],
#                 'amount': row['amount'],
#                 'up_limit': row['up_limit'],
#                 'down_limit': row['down_limit']
#             })
#         else:
#             # 如果 ts_code 不存在于 CodeInfo 中，可以选择记录日志或采取其他措施
#             print(f"Warning: ts_code '{ts_code}' not found in CodeInfo. Skipping this record.")
#
#     if records:
#         batch_size = 1000  # 定义每批次插入的数量
#         for i in range(0, len(records), batch_size):
#             batch = records[i:i + batch_size]
#             with connection.cursor() as cursor:
#                 cursor.executemany(
#                     '''
#                         INSERT IGNORE INTO HistoryPrice (ts_code_id, trade_date, `open`, `close`, `high`, `low`, pre_close,
#                         `change`, pct_chg, vol, amount, up_limit, down_limit)
#                         VALUES (%(ts_code)s, %(trade_date)s, %(open)s, %(close)s, %(high)s, %(low)s, %(pre_close)s,
#                         %(change)s, %(pct_chg)s, %(vol)s, %(amount)s, %(up_limit)s, %(down_limit)s)
#                     ''',
#                     batch
#                 )
#
#     return HttpResponse('数据写入成功')

# ChatGPT第二次优化的代码add_history_price
# def add_history_price(request):
#     if request.method == "GET":
#         return render(request, 'add_history_price.html')
#
#     pro = ts.pro_api()
#     # 从页面获取post传递过来的数据
#     trade_date = request.POST.get('trade_date')
#
#     if not trade_date:
#         return HttpResponse('请提供交易日期')
#
#     # 从数据库中获取对应的数据
#     date_is_open = TradeIsOpen.objects.filter(cal_date=trade_date).first()
#     date_is_exist = HistoryPrice.objects.get(trade_date=trade_date)
#     print(date_is_exist)
#
#     # 判断今天是否开盘
#     if date_is_open.is_open == '0' or date_is_exist:
#         return HttpResponse('今天不开盘或者数据已经存在')
#
#     trade_date = datetime.strptime(trade_date, '%Y-%m-%d').strftime('%Y%m%d')
#
#     df_limit = pro.stk_limit(trade_date=trade_date)
#
#     df_price = pro.daily(trade_date=trade_date, fields='ts_code,trade_date, open, close, high, low, '
#                                                        'pre_close, change, pct_chg, vol, amount')
#     df = pd.merge(df_price, df_limit, on=['trade_date', 'ts_code'])
#     df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d').dt.date
#
#     # 假设需要插入的 ts_code 已经在数据库中
#     code_info_dict = {code.ts_code: code for code in CodeInfo.objects.all()}
#     # 准备插入的数据
#     records = []
#     for _, row in df.iterrows():
#         ts_code = row['ts_code']
#         if ts_code in code_info_dict:
#             records.append({
#                 'ts_code': code_info_dict[ts_code].ts_code,  # 使用正确的字段名
#                 'trade_date': row['trade_date'],
#                 'open': row['open'],
#                 'close': row['close'],
#                 'high': row['high'],
#                 'low': row['low'],
#                 'pre_close': row['pre_close'],
#                 'change': row['change'],
#                 'pct_chg': row['pct_chg'],
#                 'vol': row['vol'],
#                 'amount': row['amount'],
#                 'up_limit': row['up_limit'],
#                 'down_limit': row['down_limit']
#             })
#         else:
#             print(f"Warning: ts_code '{ts_code}' not found in CodeInfo. Skipping this record.")
#
#     if records:
#         batch_size = 1000  # 定义每批次插入的数量
#         for i in range(0, len(records), batch_size):
#             batch = records[i:i + batch_size]
#             with connection.cursor() as cursor:
#                 cursor.executemany(
#                     '''
#                     INSERT IGNORE INTO HistoryPrice (ts_code_id, trade_date, `open`, `close`, `high`, `low`, pre_close,
#                     `change`, pct_chg, vol, amount, up_limit, down_limit)
#                     VALUES (%(ts_code)s, %(trade_date)s, %(open)s, %(close)s, %(high)s, %(low)s, %(pre_close)s,
#                     %(change)s, %(pct_chg)s, %(vol)s, %(amount)s, %(up_limit)s, %(down_limit)s)
#                     ''',
#                     batch
#                 )
#
#         return HttpResponse('数据写入成功')
#     return HttpResponse('数据没有正确获取，数据为空')



# 自己写的
# def add_trade_is_open(request):
#     if request.method == "GET":
#         return render(request, 'add_history_price.html')
#     start_trade_date = request.POST.get('start_trade_date')
#     end_trade_date = request.POST.get('end_trade_date')
#     pro = ts.pro_api()
#     df = pro.trade_cal(exchange='', start_date=start_trade_date, end_date=end_trade_date)
#     df['cal_date'] = pd.to_datetime(df['cal_date'], format='%Y%m%d')
#     df['pretrade_date'] = pd.to_datetime(df['pretrade_date'], format='%Y%m%d')
#
#
#     cal_date_dict = {date_is_open.cal_date: date_is_open for date_is_open in TradeIsOpen.objects.all()}
#     # 准备插入的数据
#     records = []
#     for _, row in df.iterrows():
#         cal_date = row('cal_date')
#         if cal_date not in cal_date_dict:
#             records.append(
#                 {
#                     'exchange': row['exchange'],
#                     'cal_date': row['cal_date'],
#                     'is_open': row['is_open'],
#                     'pretrade_date': row['pretrade_date']
#                 }
#             )
#
#         else:
#             print('errors')
#
#     if records:
#         batch_size = 1000  # 定义每批次插入的数量
#         for i in range(0, len(records), batch_size):
#             batch = records[i:i + batch_size]
#             with connection.cursor() as cursor:
#                 cursor.executemany(
#                     '''
#                         INSERT IGNORE INTO TradeIsOpen (exchange, cal_date, is_open, pretrade_date)
#                         VALUES (%(exchange)s, %(cal_date)s, %(is_open)s, %(pretrade_date)s)
#                     ''',
#                     batch
#                 )
#
#     return HttpResponse('数据写入成功')

