# coding: utf-8
from __future__ import unicode_literals

from django.db import models

#from rest_framework import 
    
ASSET_TYPE = (
    (1,u'物理机'),
    (2,u'虚拟机'),
    (3,'网络设备'),
    (4,'其他'),
    )
ASSET_STATUS = (
    (1,'未使用'),
    (2,'已使用'),
    )

WORK_STATUS = {}

MYSQL_STATUS = (
    (1,u'运行中'),
    (2,u'已停止'),
    (3,u'无'),
    )

class Assets(models.Model):
    ipaddr = models.CharField(max_length=255,unique=True,verbose_name='IP')
    host_style  = models.SmallIntegerField(choices=ASSET_TYPE)
    sys_version = models.CharField(max_length=50,verbose_name='操作系统')
    cpu = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    memory = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'内存')
    disk = models.CharField(max_length=1024, blank=True, null=True, verbose_name=u'硬盘')
    status = models.IntegerField(choices=ASSET_STATUS, blank=True, null=True, default=2, verbose_name=u"使用状态")
    db_instance = models.IntegerField(choices=MYSQL_STATUS, blank=True, null=True, default=3, verbose_name=u"MySQL运行状态")
    date_added = models.DateTimeField(auto_now=True, null=True)
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"备注")
    
 
class MonitorDatas(models.Model):
    hostid = models.ForeignKey(Assets,blank=True, null=True,verbose_name='主机ID')
    cpu_useage = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    memory_useage = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'内存')
    disk_useage = models.CharField(max_length=1024, blank=True, null=True, verbose_name=u'硬盘')
    run_status  = models.CharField(max_length=30,null=True,verbose_name=u'运行状态')
    date = models.DateTimeField(auto_now_add=True)
    
    
class MysqlInfo(models.Model):
    hostid = models.ForeignKey(Assets,blank=True, null=True,verbose_name='主机ID')
    alive  =  models.IntegerField(choices=MYSQL_STATUS, blank=True, null=True, default=2, verbose_name=u"运行状态")
    connections = models.CharField(max_length=30,null=True,verbose_name=u'连接使用率')
    qps_useage = models.CharField(max_length=10,null=True,verbose_name=u'查询吞吐量')
    tps_useage = models.CharField(max_length=10,null=True,verbose_name=u'写入吞吐量')
    slow_query = models.CharField(max_length=30,null=True,verbose_name=u'慢查询量')
    buffer_useage = models.CharField(max_length=30,null=True,verbose_name=u'缓存使用率')
    buffer_hitrate = models.CharField(max_length=30,null=True,verbose_name=u'缓存命中率')
    date = models.DateTimeField(auto_now_add=True)
    