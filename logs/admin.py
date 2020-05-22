from .models import ErrorLog
from django.contrib import admin


# Register your models here.
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ErrorLog._meta.get_fields() if field.auto_created is False]


admin.site.register(ErrorLog, ErrorLogAdmin)
