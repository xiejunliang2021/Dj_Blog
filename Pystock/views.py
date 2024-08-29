import pandas as pd
import tushare as ts
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection, transaction
from django.shortcuts import render, HttpResponse, redirect

from Pystock.models import CodeInfo, HistoryPrice, TradeIsOpen


def index(request):
    return render(request, 'pystock_index.html')


def py_yield(request):
    return render(request, 'pystock_yield.html')


def py_code(request):
    return render(request, 'pystock_code.html')


def py_all_yield(request):
    return render(request, 'pystock_all_yield.html')


def code_list(request):
    item_list = CodeInfo.objects.all()  # 从数据库中获取所有数据

    # 分页处理
    page = request.GET.get('page', 1)
    paginator = Paginator(item_list, 10)  # 每页显示10条数据
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'code_list.html', {'items': items})


def code_list_2(request):
    item_list = CodeInfo.objects.all()  # 从数据库中获取所有数据
    # 分页处理
    page = request.GET.get('page', 1)
    paginator = Paginator(item_list, 10)  # 每页显示10条数据
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'code_info_2.html', {'items': items})


def stock_list(request):
    query = request.GET.get('q')  # 获取搜索关键词
    if query:
        stock_info = CodeInfo.objects.filter(name__icontains=query)
    else:
        stock_info = CodeInfo.objects.all()

    return render(request, 'stock_list.html', {'stock_info': stock_info})


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
def add_history_price(request):
    if request.method == "GET":
        return render(request, 'add_history_price.html')

    pro = ts.pro_api()
    # 从页面获取post传递过来的数据
    trade_date = request.POST.get('trade_date')
    if not trade_date:
        return HttpResponse('请提供交易日期')
    print(trade_date)
    # 从数据库中获取对应的数据
    date_is_open = TradeIsOpen.objects.filter(cal_date=trade_date).first()
    print(date_is_open.is_open)
    # 判断今天是否开盘
    if date_is_open.is_open == '0':
        return HttpResponse('今天不开盘')

    df_limit = pro.stk_limit(trade_date=trade_date)
    df_price = pro.daily(trade_date=trade_date, fields='ts_code,trade_date, open, close, high, low, '
                                                       'pre_close, change, pct_chg, vol, amount')
    df = pd.merge(df_price, df_limit, on=['trade_date', 'ts_code'])
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')

    # 假设需要插入的 ts_code 已经在数据库中
    code_info_dict = {code.ts_code: code for code in CodeInfo.objects.all()}

    # 准备插入的数据
    records = []
    for _, row in df.iterrows():
        ts_code = row['ts_code']
        if ts_code in code_info_dict:
            records.append({
                'ts_code': code_info_dict[ts_code].ts_code,  # 使用正确的字段名
                'trade_date': row['trade_date'],
                'open': row['open'],
                'close': row['close'],
                'high': row['high'],
                'low': row['low'],
                'pre_close': row['pre_close'],
                'change': row['change'],
                'pct_chg': row['pct_chg'],
                'vol': row['vol'],
                'amount': row['amount'],
                'up_limit': row['up_limit'],
                'down_limit': row['down_limit']
            })
        else:
            print(f"Warning: ts_code '{ts_code}' not found in CodeInfo. Skipping this record.")

    if records:
        batch_size = 1000  # 定义每批次插入的数量
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            with connection.cursor() as cursor:
                cursor.executemany(
                    '''
                    INSERT IGNORE INTO HistoryPrice (ts_code_id, trade_date, `open`, `close`, `high`, `low`, pre_close, 
                    `change`, pct_chg, vol, amount, up_limit, down_limit)
                    VALUES (%(ts_code)s, %(trade_date)s, %(open)s, %(close)s, %(high)s, %(low)s, %(pre_close)s, 
                    %(change)s, %(pct_chg)s, %(vol)s, %(amount)s, %(up_limit)s, %(down_limit)s)
                    ''',
                    batch
                )

    return HttpResponse('数据写入成功')


def history_price_list(request):
    if request.method == 'GET':
        return render(request, 'history_price_info.html')

    ts_code = request.POST.get('ts_code')
    history_price_data = HistoryPrice.objects.filter(ts_code=ts_code)

    return render(request, 'history_price_info.html', {'history_price_data': history_price_data})


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


# ChatGPT优化后的代码
def add_trade_is_open(request):
    if request.method == "GET":
        return render(request, 'add_history_price.html')

    start_trade_date = request.POST.get('start_trade_date')
    end_trade_date = request.POST.get('end_trade_date')

    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=start_trade_date, end_date=end_trade_date)
    df['cal_date'] = pd.to_datetime(df['cal_date'], format='%Y%m%d')
    df['pretrade_date'] = pd.to_datetime(df['pretrade_date'], format='%Y%m%d')

    # 获取现有的 cal_date 集合
    existing_cal_dates = set(TradeIsOpen.objects.filter(
        cal_date__in=df['cal_date']
    ).values_list('cal_date', flat=True))

    # 准备插入的数据
    records = [
        {
            'exchange': row['exchange'],
            'cal_date': row['cal_date'],
            'is_open': row['is_open'],
            'pretrade_date': row['pretrade_date']
        }
        for _, row in df.iterrows() if row['cal_date'] not in existing_cal_dates
    ]

    # 使用事务进行批量插入
    if records:
        try:
            with transaction.atomic():
                batch_size = 1000  # 定义每批次插入的数量
                for i in range(0, len(records), batch_size):
                    batch = records[i:i + batch_size]
                    with connection.cursor() as cursor:
                        cursor.executemany(
                            '''
                            INSERT IGNORE INTO TradeIsOpen (exchange, cal_date, is_open, pretrade_date)
                            VALUES (%(exchange)s, %(cal_date)s, %(is_open)s, %(pretrade_date)s)
                            ''',
                            batch
                        )
        except Exception as e:
            # 错误处理和日志记录
            print(f"Error occurred: {e}")
            return render(request, 'add_history_price.html', {'error_message': 'Failed to add trade data'})

    # 成功插入数据后的响应
    return redirect('pystock:is_open_info')


def is_open_info(request):
    # order_by 后面的值加了一个“-”减号表示倒序
    data = TradeIsOpen.objects.all().order_by('-cal_date')

    # 设置每页显示的数据量
    paginator = Paginator(data, 10)  # 每页显示 10 条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tradedate_is_open.html', {'data': page_obj})
