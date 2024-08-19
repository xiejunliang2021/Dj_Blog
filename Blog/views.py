<<<<<<< HEAD
from django.shortcuts import render, HttpResponse, redirect
=======
from django.shortcuts import render, HttpResponse
>>>>>>> bda9a661353be63ec330624b005d0478fe0724d2
from .models import *


def index(request):
    return render(request, 'index.html')


def django_link(request):
    return render(request, 'django_link.html')


def django_return_arg(request):
    return render(request, 'django_return_arg.html')


def django_test_blog(request):
    info = TestBlog.objects.all()
<<<<<<< HEAD
    dict_data = {'data': list(info)}
    #
    return render(request, 'test_blog.html', dict_data)
    # try:
    #     User.objects.create(username='xiejunliang', password='22334455')
    #     info = '插入数据成功'
    # except Exception as e:
    #     info = '插入数据失败'
    # return render(request, 'test_blog.html', {'info': info})


def django_test_add(request):
    if request.method == 'GET':
        return render(request, 'test_add.html')
    # 在这里获取数据的时候，后面的名字要和前端传过来的名字一样，否则报错
    username = request.POST.get('username')
    password = request.POST.get('password')
    # print(username, password)
    User.objects.create(username=username, password=password)
    return redirect('/blog/user_info/')


def user_info(request):
    user_data = User.objects.all()
    return render(request, 'user_info.html', {'data': user_data})
=======
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
>>>>>>> bda9a661353be63ec330624b005d0478fe0724d2


def django_test_del(request):
    return render(request, 'test_del.html')


def django_test_update(request):
    return render(request, 'test_update.html')


def django_test_find(request):
    return render(request, 'test_find.html')
