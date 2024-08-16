from django.urls import path
from .views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('return_arg/', django_return_arg, name='django_return_arg'),
    path('django/', django_link, name='django'),
    path('test/', django_test_blog, name='django_test'),
    path('add/', django_test_add, name='django_add'),
    path('del/', django_test_del, name='django_del'),
    path('update/', django_test_update, name='django_update'),
    path('find/', django_test_find, name='django_find'),
]



