from django.contrib import admin
from .models import AddCustom
from .models import AddApp
from .models import AddAppserver
from .models import AddEnvironment
from .models import AddNode
from .models import AddProject
# Register your models here.
admin.site.register(AddCustom)
admin.site.register(AddApp)
admin.site.register(AddAppserver)
admin.site.register(AddEnvironment)
admin.site.register(AddNode)
admin.site.register(AddProject)