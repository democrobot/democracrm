from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('us/', views.us_index),
    path('us/us.geojson', views.us_us_geojson),
    path('us/pa/', views.us_pa_index),
    path('us/pa.geojson', views.us_pa_geojson)
]
