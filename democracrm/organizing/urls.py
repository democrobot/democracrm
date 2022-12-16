from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('base', views.base),
    path('platform/', views.platform),
    path('campaigns/', views.campaign_list),
    path('campaigns/<int:campaign_id>', views.campaign_detail),
]
