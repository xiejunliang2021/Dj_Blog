from django.shortcuts import render, HttpResponse
from .models import *


def index(request):

    return render(request, 'index.html')


def django_link(request):

    return render(request, 'django_link.html')


def django_return_arg(request):

    return render(request, 'django_return_arg.html')


def django_test_blog(request):
    info = TestBlog.objects.all()
    # dict_data = {'data': info}

    return render(request, 'test_blog.html', {'data': info})


def django_test_add(request):
    # 当用户以GET方式访问的时候，展示给用户的是form表单，让用户来添加数据，
    if request.method == 'GET':       # 注意这里的GET的写法，全部大写
        return render(request, 'test_add.html')

    # 当用户添加了数据以后，点击提交以后数据会以POST的方式提交回来，我们进行接收，并进行创建
    username = request.POST.get('username')
    password = request.POST.get('password')
    User.objects.create(username=username, password=password)
    #
    return HttpResponse("添加数据成功")


def django_test_del(request):

    return render(request, 'test_del.html')


def django_test_update(request):

    return render(request, 'test_update.html')


def django_test_find(request):

    return render(request, 'test_find.html')

















