# Generated by Django 4.2 on 2024-08-21 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StockCode",
            fields=[
                (
                    "ts_code",
                    models.CharField(
                        max_length=16,
                        primary_key=True,
                        serialize=False,
                        verbose_name="股票代码",
                    ),
                ),
                ("symbol", models.CharField(max_length=16, verbose_name="股票代码数字")),
                ("name", models.CharField(max_length=16, verbose_name="股票名称")),
                ("area", models.CharField(max_length=16, verbose_name="地区")),
                ("industry", models.CharField(max_length=16, verbose_name="行业")),
                ("list_date", models.DateField(verbose_name="上市时间")),
                ("market", models.CharField(max_length=16, verbose_name="市场类型")),
                ("list_status", models.CharField(max_length=16, verbose_name="上市状态")),
                ("is_hs", models.CharField(max_length=16, verbose_name="是否沪港通")),
            ],
        ),
        migrations.CreateModel(
            name="HistoryPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "open",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="开盘价"
                    ),
                ),
                (
                    "close",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="收盘价"
                    ),
                ),
                (
                    "high",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="最高价"
                    ),
                ),
                (
                    "low",
                    models.DecimalField(
                        decimal_places=2, max_digits=6, verbose_name="最低价"
                    ),
                ),
                (
                    "ts_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Pystock.stockcode",
                    ),
                ),
            ],
        ),
    ]
