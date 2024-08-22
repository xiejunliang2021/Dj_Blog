from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Pystock.models import StockCode


def index(request):

    return render(request, 'pystock_index.html')


def py_yield(request):

    return render(request, 'pystock_yield.html')


def py_code(request):

    return render(request, 'pystock_code.html')


def py_all_yield(request):

    return render(request, 'pystock_all_yield.html')


def code_list(request):
    item_list = StockCode.objects.all()  # 从数据库中获取所有数据

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


