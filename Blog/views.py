import json

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django import forms
from Blog.models import *
from Dj_Blog.utils.bootstrap import BootstrapModelForm
from Dj_Blog.utils.encrypt import md5


def layout(request):
    return render(request, 'index.html')


def index(request):
    return render(request, 'index.html')


def django_link(request):
    return render(request, 'django_link.html')


def django_return_arg(request):
    return render(request, 'django_return_arg.html')


def django_test_blog(request):
    info = TestBlog.objects.all()
    dict_data = {'data': list(info)}
    return render(request, 'test_blog.html', dict_data)
    # try:
    #     User.objects.create(username='xiejunliang', password='22334455')
    #     info = '插入数据成功'
    # except Exception as e:
    #     info = '插入数据失败'
    # return render(request, 'test_blog.html', {'info': info})


def user_info(request):
    user_data = User.objects.all()
    return render(request, 'user_info.html', {'data': user_data})


def django_test_add(request):
    # 当用户以GET方式访问的时候，展示给用户的是form表单，让用户来添加数据，
    if request.method == 'GET':  # 注意这里的GET的写法，全部大写
        return render(request, 'test_add.html')

    # 当用户添加了数据以后，点击提交以后数据会以POST的方式提交回来，我们进行接收，并进行创建
    username = request.POST.get('username')
    password = request.POST.get('password')
    User.objects.create(username=username, password=password)

    return redirect('blog:user_info')


def django_test_del(request, nid):
    User.objects.filter(id=nid).delete()

    # 注意这里不能用render，应该用redirect,用redirect的时候后面不能有request
    return redirect('blog:user_info')


def update_user(request, nid):
    if request.method == "GET":
        data = User.objects.filter(id=nid).first()
        return render(request, 'update_user.html', {"data": data})
    username = request.POST.get('username')
    password = request.POST.get('password')
    User.objects.filter(id=nid).update(username=username, password=password)
    return redirect('blog:user_info')


def django_test_find(request):
    return render(request, 'test_find.html')


# modelform 实例
class UserModelForm(BootstrapModelForm):
    # 新生成校验规则，如果字符数少于三个则报错
    password = forms.CharField(min_length=3,
                               label='密码',
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'password']
        # 以下方法是每个字段进行添加
        # widgets = {
        #     'username': forms.TextInput(attrs={"class": "form-control"}),
        #     'password': forms.PasswordInput(attrs={"class": "form-control"})
        # }

    # 以下方法是通过重写方法来添加, 优化之前的代码
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     # 循环找到插件，添加class:form-control
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "form-control"}


def user_add_modelform(request):
    """ 添加用户，modelform 版本 """

    if request.method == 'GET':
        form = UserModelForm()

        return render(request, 'user_add_modelform.html', {'form': form})

    # 用户通过post方式提交，对数据进行校验
    form = UserModelForm(data=request.POST)
    # 如果校验成功
    if form.is_valid():
        # 将校验合法的数据存到数据库中
        form.save()
        # print(form.cleaned_data)
        return redirect('blog:user_info')
    # 如果校验失败
    else:
        print(form.errors)
    return HttpResponse('chenggong')


# chatgpt生成的方法
def user_add_model_form(request):
    """ 添加用户，modelform 版本 """
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            # 重定向或其他逻辑
            return redirect('blog:user_info')
    else:
        form = UserModelForm()

    return render(request, 'user_add_modelform.html', {'form': form})


class AdminModelForm(BootstrapModelForm):
    # 自己定义的字段
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            # 后面的参数就时当密码输入不一致以后刷新页面后会保留原来的数据
            'password': forms.PasswordInput(render_value=True),

        }

    def clean_password(self):
        password = self.cleaned_data['password']

        return md5(password)

    def clean_confirm_password(self):
        # 在这里也可以获取cleaned_data
        # print(self.cleaned_data)
        pwd = self.cleaned_data.get('password')
        # 由于执行顺序按照['username', 'password', 'confirm_password']，所以这时候我们拿到的字段password已经时MD5加密过的
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        # 当两次输入的密码不一致的时候，页面返回错误，将两次输入的密码的密文进行比较
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')

        # return之后的数据将会保存到cleaned_data中，当执行form.save后将保存到数据库中
        return md5(confirm_pwd)


def admin_add(request):
    """ 添加管理员 """
    if request.method == 'POST':
        form = AdminModelForm(request.POST)
        if form.is_valid():
            # 验证通过后里面的数据 form.cleaned_data
            # print(form.cleaned_data)
            form.save()
            # 重定向或其他逻辑
            return redirect('blog:admin_info')
    else:
        form = AdminModelForm()

    return render(request, 'change.html', {'title': "新建管理员", 'form': form})


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = Admin
        fields = ["username"]


def admin_info(request):
    queryset = Admin.objects.all()
    return render(request, 'admin_info.html', {'context': queryset})


def admin_delete(request, nid):
    """ 删除管理员 """

    Admin.objects.filter(id=nid).delete()

    return redirect('blog:admin_info')


def admin_edit(request, nid):
    """ 编辑管理员 """
    row_obj = Admin.objects.filter(id=nid).first()
    if not row_obj:
        return HttpResponse("数据不存在")

    title = '编辑管理员'
    """ 当我们的编辑的form和添加的form所用的数据一致的时候，我们可以用同一个form，
                如果不是，那么我们就要为我们的编辑页面重新编写一个form     """
    if request.method == "GET":
        # instance = row_obj  在编辑页面显示默认值
        form = AdminEditModelForm(instance=row_obj)

        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()

        return redirect("blog:admin_info")

    return render(request, 'change.html', {"form": form, "title": title})


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(label='确认密码')
    old_password = forms.CharField(label='请输入原来的密码')

    class Meta:
        model = Admin
        fields = ['old_password', 'password', 'confirm_password']

    def clean_old_password(self):
        """ 当输入的密码和数据库中的密码不一致的时候报错 """
        if not Admin.objects.filter(id=self.instance.pk, password=md5(self.cleaned_data.get('old_password'))).exists():
            raise ValidationError("请你输入正确的密码")

    def clean_password(self):
        """ cleaned_data 可以获取用户输入的数据 """
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        """
        下面的写法是错误的，由于这时候获取的password已经是经过加密的，所以我们比较的经过加密后的字符串
        pwd = self.cleaned_data.get("password")
        confirm_pwd = self.cleaned_data.get("confirm_password")
        if pwd == confirm_pwd:
            return md5(confirm_pwd)
        raise ValidationError('两次密码不一致')

        """
        pwd = self.cleaned_data.get("password")
        confirm_pwd = self.cleaned_data.get("confirm_password")
        if pwd != md5(confirm_pwd):
            raise ValidationError("两次输入密码不一致")
        return md5(confirm_pwd)


def admin_reset(request, nid):
    row_obj = Admin.objects.filter(id=nid).first()
    if not row_obj:
        return HttpResponse("数据不存在")
    title = f"重置--> {row_obj.username} 密码"
    """ 当我们的编辑的form和添加的form所用的数据一致的时候，我们可以用同一个form，
                如果不是，那么我们就要为我们的编辑页面重新编写一个form     """
    if request.method == "GET":
        # instance = row_obj  在编辑页面显示默认值
        form = AdminResetModelForm

        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_obj)

    if form.is_valid():
        form.save()

        return redirect("blog:admin_info")

    return render(request, 'change.html', {"form": form, "title": title})


class LoginForms(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput
    )

    def clean_password(self):
        return md5(self.cleaned_data.get("password"))


def login(request):
    # 一定要记住下面的写法，很重要，从页面获取数据
    form = LoginForms(data=request.POST)
    if form.is_valid():
        # 原始的写法，由于传入的是字典，我们就可以用下面的方式进行解包传递数据
        # obj = Admin.objects.filter(username=form.cleaned_data.get("username"),
        # password=form.cleaned_data.get("password"))
        obj = Admin.objects.filter(**form.cleaned_data)
        if obj.first():
            request.session['info'] = {"id": obj.first().id, 'username': obj.first().username}
            return redirect("blog:admin_info")
        else:
            # 主动添加错误，前面是field，后面是错误信息
            form.add_error(field="password", error="用户名或密码错误")
            return render(request, 'login.html', {"form": form})
    return render(request, 'login.html', {"form": form})


def test_ajax(request):
    return render(request, 'test_ajax.html')


@csrf_exempt
def res_ajax(request):
    # 当用户通过ajax请求向这里发送了get请求后，我们可以通过下面的方法来接收数据
    # name = request.GET['name']
    # print(name)
    # name = request.POST
    # print(name)
    # 将数据转化成json格式发送给前端页面， 由于这样写比较麻烦，Django自带了json转换的jsonresponse
    # data_dict = {"status": True, 'list': [1, 2, 3, 4]}
    # json_data = json.dumps(data_dict)
    # return HttpResponse('welcome back！！！')
    data_dict = request.POST
    return JsonResponse(data_dict)
