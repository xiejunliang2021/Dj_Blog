from django.urls import path
from .views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('return_arg/', django_return_arg, name='django_return_arg'),
    path('django/', django_link, name='django'),
    path('test/', django_test_blog, name='django_test'),
    path('add/', django_test_add, name='django_add'),
    path('del/<int:nid>', django_test_del, name='django_del'),
    path('update/<int:nid>/user/', update_user, name='update_user'),
    path('find/', django_test_find, name='django_find'),
    path('user_info/', user_info, name='user_info'),
    path('user_add_modelform/', user_add_modelform, name='user_add_modelform'),
    path('user_add_model_form/', user_add_model_form, name='user_add_model_form'),
    path('admin_add/', admin_add, name='admin_add'),
]



