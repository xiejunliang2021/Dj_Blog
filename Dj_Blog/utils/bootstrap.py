# -*- coding: UTF-8 -*-
'''
@Project ：Dj_Blog 
@File ：bootstrap.py
@Author ：Anita_熙烨
@Date ：2024/9/2 21:43 
@JianShu : 人生在世不容易，求佛祖保佑我们全家苦难不近身，平安健康永相随，
            远离小人讹诈，万事如意，心想事成！！！
'''

from django import forms


class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置样式
        for name, field in self.fields.items():
            # 字段中原来有的属性则保留原来的属性，如果没有我们就进行添加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }
