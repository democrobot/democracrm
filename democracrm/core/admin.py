from django.contrib import admin

from .models import GeographicArea


# class MyAdminSite(admin.AdminSite):
#     site_header = 'Monty Python administration'
#
#
# admin_site = MyAdminSite(name='myadmin')
# #admin_site.register(MyModel)

@admin.register(GeographicArea)
class GeographicAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
