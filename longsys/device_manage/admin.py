from django.contrib import admin
from device_manage.models import *

# Register your models here.
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(User)
admin.site.register(TestRequirements)
admin.site.register(RequirementsRecord)
