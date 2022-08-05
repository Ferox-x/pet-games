from django.contrib import admin


class SchulteModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'record', 'date']

class StroopModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'record', 'date']
