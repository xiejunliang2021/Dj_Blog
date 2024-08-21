from django.db import models


class StockCode(models.Model):
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
    ts_code = models.ForeignKey(to=StockCode, to_field='ts_code', on_delete=models.CASCADE)
    open = models.DecimalField(verbose_name='开盘价', max_digits=6, decimal_places=2)
    close = models.DecimalField(verbose_name='收盘价', max_digits=6, decimal_places=2)
    high = models.DecimalField(verbose_name='最高价', max_digits=6, decimal_places=2)
    low = models.DecimalField(verbose_name='最低价', max_digits=6, decimal_places=2)




