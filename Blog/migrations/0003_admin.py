# Generated by Django 4.2 on 2024-09-03 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_alter_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=30, verbose_name='用户名')),
                ('password', models.CharField(default='', max_length=50, verbose_name='密码')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
    ]
