from django.contrib import admin

from .models import (
    OrganizationGroup,
    Organization,
    CampaignCategory,
    Campaign,
    CampaignMilestone,
    Chapter,
    PersonGroup,
    Person
)


@admin.register(OrganizationGroup)
class OrganizationGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'relationship', 'region', 'url']


@admin.register(CampaignCategory)
class CampaignCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'priority', 'status', 'target_supporters_count', 'target_undecided_count', 'target_opposers_count']
    save_as = True


@admin.register(CampaignMilestone)
class CampaignMilestoneAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'status']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'org_account', 'region']


@admin.register(PersonGroup)
class PersonGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user_account', 'last_name', 'first_name', 'org_account']




