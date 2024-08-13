from django.urls import path
from Pystock.views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('yield/', py_yield, name='yield'),
    path('code/', py_code, name='code'),
    path('all_yield/', py_all_yield, name='all_yield')
]





