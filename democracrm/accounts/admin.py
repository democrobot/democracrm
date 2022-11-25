from django.contrib import admin

from .models import UserAccount, OrganizationAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


@admin.register(OrganizationAccount)
class OrganizationAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


