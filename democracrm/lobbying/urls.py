from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('public-officials', views.officials_directory),
    path('public-official/<int:official_id>', views.official_profile),
]