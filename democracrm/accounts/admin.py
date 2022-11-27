from django.contrib import admin

from .models import UserAccount, OrganizationAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'is_active', 'is_staff', 'is_superuser']


@admin.register(OrganizationAccount)
class OrganizationAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


