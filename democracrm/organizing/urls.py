from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('base', views.base),
    path('campaigns/', views.campaign_dashboard),
    path('campaigns/<int:campaign_id>', views.campaign_detail),
    path('campaigns/<int:campaign_id>/timeline', views.campaign_timeline),
]
