from django.db import models

# Create your models here.
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
    
    def __str__(self):
        return("/".join([self.username,self.first_name]))
        
class PpsWarntype(models.Model):
    warntype = models.CharField(max_length=30, blank=True, null=True,verbose_name='预警类别')
    warnname = models.CharField(max_length=30, blank=True, null=True,verbose_name='预警名字')
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='uid',db_column='userid', blank=True, null=True,verbose_name='预警处理人')
    auduserid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='auduserid', blank=True, null=True,verbose_name='预警审核人')
    class Meta:
        managed = False
        db_table = 'pps_warntype'
        verbose_name_plural='报警负责人设置'  
        verbose_name='报警负责人设置'
    
    def __str__(self):
        return("/".join([str(self.userid),self.warntype,self.warnname,str(self.auduserid)]))

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'
    
    def __str__(self):
        return(self.name)
'''        
class PpsAuditGroup(models.Model):
    gid = models.ForeignKey(AuthGroup, models.DO_NOTHING, related_name='gid',db_column='gid', blank=True, null=True,verbose_name='被审核组')
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid', blank=True, null=True,verbose_name='审核人')

    class Meta:
        managed = False
        db_table = 'pps_audit_group'  
        verbose_name_plural='审核组设置'  
        verbose_name='审核组设置' 
    def __str__(self):
        return("/".join([str(self.gid),str(self.uid)]))     
'''


class PpsWarnlevel(models.Model):
    level = models.IntegerField(blank=True, null=True,verbose_name='预警等级ID')
    levelname = models.CharField(max_length=30, blank=True, null=True,verbose_name='预警等级名字')

    class Meta:
        managed = False
        db_table = 'pps_warnlevel'
        verbose_name_plural='预警等级设置'  
        verbose_name='预警等级设置'   

    def __str__(self):
        return("/".join([str(self.level),str(self.levelname)]))         