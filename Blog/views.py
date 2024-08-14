from django.shortcuts import render


def index(request):

    return render(request, 'index.html')


def django_link(request):

    return render(request, 'django_link.html')


def django_return_arg(request):

    return render(request, 'django_return_arg.html')





















