from django.shortcuts import render


def index(request):

    return render(request, 'pystock_index.html')


def py_yield(request):

    return render(request, 'pystock_yield.html')


def py_code(request):

    return render(request, 'pystock_code.html')


def py_all_yield(request):

    return render(request, 'pystock_all_yield.html')