from django.db import models


class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=30, default='')
    password = models.CharField(verbose_name='密码', max_length=50, default='')
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    update_date = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return "%s--%s" % (self.username, self.password)


class TestBlog(models.Model):
    author = models.AutoField(primary_key=True)
    age = models.IntegerField(default=18)
    edit_date = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(default='2000-01-01', blank=True)
    info = models.TextField(blank=True)
    img1 = models.ImageField(upload_to='static/images/')


    class Meta:
        db_table = 'test'
