from django.shortcuts import render
from .models import *


def index(request):

    return render(request, 'index.html')


def django_link(request):

    return render(request, 'django_link.html')


def django_return_arg(request):

    return render(request, 'django_return_arg.html')


def django_test_blog(request):
    info = TestBlog.objects.all()
    dict_data = {'data': list(info)}

    return render(request, 'test_blog.html', dict_data)


def django_test_add(request):

    return render(request, 'test_add.html')


def django_test_del(request):

    return render(request, 'test_del.html')


def django_test_update(request):

    return render(request, 'test_update.html')


def django_test_find(request):

    return render(request, 'test_find.html')

















