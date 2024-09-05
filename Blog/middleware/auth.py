# -*- coding: UTF-8 -*-
'''
@Project ：Dj_Blog 
@File ：auth.py
@Author ：Anita_熙烨
@Date ：2024/9/4 20:58 
@JianShu : 人生在世不容易，求佛祖保佑我们全家苦难不近身，平安健康永相随，
            远离小人讹诈，万事如意，心想事成！！！
'''
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 排除那些不需要登录就可以访问的页面
        # 获取当前用户请求的Url（request.path_info)
        # 当用户访问路径为login的url的时候直接返回空值
        if request.path_info == '/login/':
            return
        # 读取当前用户的session信息，如果有则继续，如果没有，则返回登录
        info_dict = request.session.get("info")
        if not info_dict:
            return redirect("/login/")












