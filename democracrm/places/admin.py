from django.contrib import admin

from .models import Boundary, Region, RegionGroup, Site, SiteGroup, Location


@admin.register(Boundary)
class BoundaryAdmin(admin.ModelAdmin):
    list_display = ['name', 'geoid', 'geoidfq', 'namelsad', 'lsy', 'aland', 'awater', 'level']
    search_fields = ["name"]
    list_filter = ['parent', 'level']


@admin.register(RegionGroup)
class RegionGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(SiteGroup)
class SiteGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_physical_address']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'site']