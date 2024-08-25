from django.db import models
from django.utils import timezone


class CodeInfo(models.Model):
    ts_code = models.CharField(max_length=16, primary_key=True, verbose_name='股票代码')
    symbol = models.CharField(max_length=16, verbose_name='股票代码数字')
    name = models.CharField(max_length=16, verbose_name='股票名称')
    area = models.CharField(max_length=16,verbose_name='地区')
    industry = models.CharField(verbose_name='行业',max_length=16)
    list_date = models.DateField(verbose_name='上市时间')
    market = models.CharField(verbose_name='市场类型',max_length=16)
    list_status = models.CharField(verbose_name='上市状态',max_length=16)
    is_hs = models.CharField(verbose_name='是否沪港通', max_length=16)


class HistoryPrice(models.Model):
    ts_code = models.ForeignKey(to=CodeInfo, to_field='ts_code', on_delete=models.CASCADE)
    trade_date = models.CharField(verbose_name='交易日期', max_length=32, default=timezone.now)
    open = models.DecimalField(verbose_name='开盘价', max_digits=6, decimal_places=2, default=0.01)
    close = models.DecimalField(verbose_name='收盘价', max_digits=6, decimal_places=2, default=0.01)
    high = models.DecimalField(verbose_name='最高价', max_digits=6, decimal_places=2, default=0.01)
    low = models.DecimalField(verbose_name='最低价', max_digits=6, decimal_places=2, default=0.01)
    pre_close = models.DecimalField(verbose_name='昨日收盘价', max_digits=6, decimal_places=2, default=0.01)
    change = models.DecimalField(verbose_name='涨跌额', max_digits=5, decimal_places=2, default=0.01)
    pct_chg = models.DecimalField(verbose_name='涨跌幅', max_digits=6, decimal_places=2, default=0.01)
    vol = models.DecimalField(verbose_name='成交量', max_digits=15, decimal_places=2, default=0.01)
    amount = models.DecimalField(verbose_name='成交额', max_digits=15, decimal_places=2, default=0.01)

    class Meta:
        db_table = 'HistoryPrice'


class TestCode(models.Model):
    ts_code = models.ForeignKey(to=CodeInfo, to_field='ts_code', on_delete=models.CASCADE)
    trade_date = models.CharField(verbose_name='交易日期', max_length=32, default=timezone.now)
    open = models.DecimalField(verbose_name='开盘价', max_digits=6, decimal_places=2, default=0.01)
    close = models.DecimalField(verbose_name='收盘价', max_digits=6, decimal_places=2, default=0.01)
    high = models.DecimalField(verbose_name='最高价', max_digits=6, decimal_places=2, default=0.01)
    low = models.DecimalField(verbose_name='最低价', max_digits=6, decimal_places=2, default=0.01)

    class Meta:
        db_table = 'TestCode'






