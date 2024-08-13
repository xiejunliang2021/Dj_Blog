from django.urls import path
from Blog.views import *


urlpatterns = [
    path('index/', index, name='index')
]



