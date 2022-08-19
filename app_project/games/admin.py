from django.contrib import admin

from games.models import StroopModel, SchulteModel


class SchulteModelAdmin(admin.ModelAdmin):
    """Админ панель Schulte."""
    list_display = ['user', 'record', 'date']
    list_filter = ['user', 'date']

class StroopModelAdmin(admin.ModelAdmin):
    """Админ панель Stroop."""
    list_display = ['user', 'record', 'date']
    list_filter = ['user', 'date']


admin.site.register(StroopModel, StroopModelAdmin)
admin.site.register(SchulteModel, SchulteModelAdmin)
