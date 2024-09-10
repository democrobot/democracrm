from django.contrib import admin
#from django.contrib.admin import 

from .models import (
    ImportDataSource,
    ImportDataSet,
)

@admin.register(ImportDataSource)
class ImportDataSourceAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ImportDataSet)
class ImportDataSetAdmin(admin.ModelAdmin):
    list_display = ['name']
