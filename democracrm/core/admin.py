from django.contrib import admin

from .models import (GeographicArea, Site, Location,
                     ContactRole, ContactInfo, Comment)


# class MyAdminSite(admin.AdminSite):
#     site_header = 'Monty Python administration'
#
#
# admin_site = MyAdminSite(name='myadmin')
# #admin_site.register(MyModel)


@admin.register(GeographicArea)
class GeographicAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'level']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ContactRole)
class ContactRoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_on', 'updated_on']
