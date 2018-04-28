from django.contrib import admin
from .models import PpsWarntype
#from .models import PpsAuditGroup
from .models import PpsWarnlevel
from .models import PpsEnvitype
# Register your models here.
    
admin.site.register(PpsWarntype)
#admin.site.register(PpsAuditGroup)
admin.site.register(PpsWarnlevel)
admin.site.register(PpsEnvitype)