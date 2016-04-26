from django.contrib import admin

from . import models


#class QueryAdmin(admin.ModelAdmin):
#    list_display = ('text', 'created')


admin.site.register(models.Status)
admin.site.register(models.Project)
admin.site.register(models.Transition)
