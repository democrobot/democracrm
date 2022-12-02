from django.contrib import admin

from .models import Contact, ContactRole, ContactGroup


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name']


@admin.register(ContactRole)
class ContactRoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
