from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from Pystock.models import CodeInfo, TestCode
import pandas as pd
import tushare as ts


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


def add_history_price(request):
    if request.method == "GET":
        return render(request, 'add_history_price.html')

    pro = ts.pro_api()
    trade_date = request.POST.get('trade_date')
    df = pro.daily(trade_date=trade_date, fields='ts_code,trade_date, open, close, high, low')
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
                'low': row['low']
            })
        else:
            # 如果 ts_code 不存在于 CodeInfo 中，可以选择记录日志或采取其他措施
            print(f"Warning: ts_code '{ts_code}' not found in CodeInfo. Skipping this record.")

    if records:
        batch_size = 1000  # 定义每批次插入的数量
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            with connection.cursor() as cursor:
                cursor.executemany(
                    '''
                        INSERT IGNORE INTO TestCode (ts_code_id, trade_date, open, close, high, low)
                        VALUES (%(ts_code)s, %(trade_date)s, %(open)s, %(close)s, %(high)s, %(low)s)
                    ''',
                    batch
                )

    return HttpResponse('数据写入成功')



# def add_history_price(request):
#     if request.method == "GET":
#         return render(request, 'add_history_price.html')
#
#     pro = ts.pro_api()
#     trade_date = request.POST.get('trade_date')
#     df = pro.daily(trade_date=trade_date, fields='ts_code,trade_date, open, close, high, low')
#     df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
#     print(df)
#     # 创建TestCode实例的列表
#     test_code_instances = [
#         TestCode(
#             ts_code=CodeInfo.objects.get(ts_code=row['ts_code']),  # 假设CodeInfo中已经有这些ts_code
#             trade_date=row['trade_date'],
#             open=row['open'],
#             close=row['close'],
#             high=row['high'],
#             low=row['low']
#         )
#         for _, row in df.iterrows()
#     ]
#     TestCode.objects.bulk_create(test_code_instances)
#
#     return HttpResponse('数据写入成功')
