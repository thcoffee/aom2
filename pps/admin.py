from django.contrib import admin
from .models import PpsWarntype
from .models import PpsAuditGroup
# Register your models here.
    
admin.site.register(PpsWarntype)
admin.site.register(PpsAuditGroup)