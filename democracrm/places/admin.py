from django.contrib import admin

from .models import Boundary, Region, Site, Location


@admin.register(Boundary)
class BoundaryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'level']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_physical_address']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'site']