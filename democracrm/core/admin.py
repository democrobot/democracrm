from django.contrib import admin

from .models import (GeographicBoundary, GeographicRegion, Site, Location,
                     ContactRole, ContactInfo, Comment, SocialMediaAccount)


# class MyAdminSite(admin.AdminSite):
#     site_header = 'Monty Python administration'
#
#
# admin_site = MyAdminSite(name='myadmin')
# #admin_site.register(MyModel)


@admin.register(GeographicBoundary)
class GeographicBoundaryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'level']


@admin.register(GeographicRegion)
class GeographicRegionAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_physical_address']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'site']


@admin.register(ContactRole)
class ContactRoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_on', 'updated_on']


@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['handle', 'platform', 'url']
