from django.contrib import admin

# from .models import MyModel


class MyAdminSite(admin.AdminSite):
    site_header = 'Monty Python administration'


admin_site = MyAdminSite(name='myadmin')
#admin_site.register(MyModel)
