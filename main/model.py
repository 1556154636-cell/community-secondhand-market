#coding:utf-8
from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    class Meta:
        abstract = True
