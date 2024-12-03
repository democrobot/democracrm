from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    #path('us/', views.us_index),
    path('us/pa/', views.us_pa_index),
    path('us/pa/map', views.us_pa_map),
    path('us/pa.geojson', views.us_pa_geojson)
]
