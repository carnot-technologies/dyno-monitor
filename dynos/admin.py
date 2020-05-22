from .models import App
from .models import Dyno
from django.contrib import admin


# Register your models here.
class AppAdmin(admin.ModelAdmin):
    list_display = [field.name for field in App._meta.get_fields() if field.auto_created is False]


class DynoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Dyno._meta.get_fields() if field.auto_created is False]


admin.site.register(App, AppAdmin)
admin.site.register(Dyno, DynoAdmin)
