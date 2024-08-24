from django.urls import path
from Pystock.views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('yield/', py_yield, name='yield'),
    path('code/', py_code, name='code'),
    path('all_yield/', py_all_yield, name='all_yield'),
    path('code_info/', code_list, name='code_info'),
    path('code_info_2/', code_list_2, name='code_info_2'),
    path('stock_list/', stock_list, name='stock_list'),
    path('add_historyprice/', add_history_price, name='history_price')
]





