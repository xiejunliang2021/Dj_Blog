from django.urls import path
from Blog.views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('return_arg/', django_return_arg, name='django_return_arg'),
    path('django/', django_link, name='django')
]



