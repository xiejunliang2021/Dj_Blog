# -*- coding: UTF-8 -*-
'''
@Project ：Dj_Blog 
@File ：encrypt.py
@Author ：Anita_熙烨
@Date ：2024/9/3 20:00 
@JianShu : 人生在世不容易，求佛祖保佑我们全家苦难不近身，平安健康永相随，
            远离小人讹诈，万事如意，心想事成！！！
'''


import hashlib
from django.conf import settings


def md5(data_str):

    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_str.encode('utf-8'))

    return obj.hexdigest()

