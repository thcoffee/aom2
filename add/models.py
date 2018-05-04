from django.db import models

# Create your models here.
class AddApp(models.Model):
    appid = models.AutoField(primary_key=True)
    appname = models.CharField(max_length=30, blank=True, null=True)
    appcname = models.CharField(max_length=30, blank=True, null=True)
    projectid = models.ForeignKey('AddProject', models.DO_NOTHING, db_column='projectid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'add_app'
        verbose_name_plural='应用配置'  
        verbose_name='应用配置'

class AddAppserver(models.Model):
    appserverid = models.AutoField(primary_key=True)
    appservername = models.CharField(max_length=30, blank=True, null=True)
    appserverparams = models.TextField(blank=True, null=True)
    nodeid = models.ForeignKey('AddNode', models.DO_NOTHING, db_column='nodeid', blank=True, null=True)
    appid = models.ForeignKey(AddApp, models.DO_NOTHING, db_column='appid', blank=True, null=True)
    envid = models.ForeignKey('AddEnvironment', models.DO_NOTHING, db_column='envid', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'add_appserver'
        verbose_name_plural='应用服务器配置'  
        verbose_name='应用服务器配置'

class AddCustom(models.Model):
    customid = models.AutoField(primary_key=True)
    customname = models.CharField(max_length=30, blank=True, null=True)
    customcname = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'add_custom'
        verbose_name_plural='客户配置'  
        verbose_name='客户配置'

class AddEnvironment(models.Model):
    envid = models.AutoField(primary_key=True)
    envname = models.CharField(max_length=30, blank=True, null=True)
    envcname = models.CharField(max_length=30, blank=True, null=True)
    projectid = models.ForeignKey('AddProject', models.DO_NOTHING, db_column='projectid', blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'add_environment'
        verbose_name_plural='环境配置'  
        verbose_name='环境配置'

class AddNode(models.Model):
    nodeid = models.AutoField(primary_key=True)
    nodekey = models.CharField(max_length=30, blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'add_node'
        verbose_name_plural='节点配置'  
        verbose_name='节点配置'

class AddProject(models.Model):
    projectid = models.AutoField(primary_key=True)
    projectname = models.CharField(max_length=30, blank=True, null=True)
    projectcname = models.CharField(max_length=30, blank=True, null=True)
    customid = models.ForeignKey(AddCustom, models.DO_NOTHING, db_column='customid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'add_project'
        verbose_name_plural='项目配置'  
        verbose_name='项目配置'