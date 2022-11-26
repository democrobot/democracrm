from django.contrib import admin

from .models import (
    Organization,
    Person,
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
    list_display = ['title', 'org_account']


@admin.register(PlatformCategory)
class PlatformCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'order']


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'priority', 'status', 'target_supporters_count', 'target_undecided_count', 'target_opposers_count']
    save_as = True


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user_account', 'last_name', 'first_name', 'org_account']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'org_account', 'region']

