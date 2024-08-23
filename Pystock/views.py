from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Pystock.models import CodeInfo


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




