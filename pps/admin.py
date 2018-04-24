from django.contrib import admin
from .models import PpsWarntype
#from .models import PpsAuditGroup
from .models import PpsWarnlevel
# Register your models here.
    
admin.site.register(PpsWarntype)
#admin.site.register(PpsAuditGroup)
admin.site.register(PpsWarnlevel)