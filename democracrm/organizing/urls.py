from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('base', views.base),
    path('campaigns/', views.campaign_dashboard),
    path('campaigns/<int:campaign_id>', views.campaign_detail),
    path('campaigns/<int:campaign_id>/timeline', views.campaign_timeline),
    path('people/', views.people_dashboard),
    path('people/<int:person_id>', views.person_profile),
    path('organizations/', views.organizations_dashboard),
    path('organizations/<int:organization_id>', views.organization_profile),
]
