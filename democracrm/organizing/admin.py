from django.contrib import admin

from .models import (
    Organization,
    Member,
    Chapter,
    Platform,
    PlatformCategory,
    Campaign,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'relationship', 'url']


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization']


@admin.register(PlatformCategory)
class PlatformCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'order']


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'priority', 'status']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_name', 'first_name', 'organization']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'region']

