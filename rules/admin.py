from .models import HError
from .models import RError
from django.contrib import admin


# Register your models here.
class HErrorAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('log_source', 'log_dyno')
        return ('dyno_fk', 'category', 'log_source', 'log_dyno')

    list_display = [field.name for field in HError._meta.get_fields() if field.auto_created is False]


class RErrorAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('log_source', 'log_dyno')
        return ('dyno_fk', 'category', 'log_source', 'log_dyno')

    list_display = [field.name for field in RError._meta.get_fields() if field.auto_created is False]


admin.site.register(HError, HErrorAdmin)
admin.site.register(RError, RErrorAdmin)
