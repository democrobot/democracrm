from django.shortcuts import render

from .models import Campaign


def index(request):
    return render(request, 'organizing/index.html', {})


def base(request):
    return render(request, 'organizing/base.html', {})


def campaign_list(request):
    campaigns = Campaign.objects.all()
    context = {'campaigns': campaigns}
    return render(request, 'organizing/campaign_list.html', context)


def campaign_detail(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    context = {'campaign': campaign}
    return render(request, 'organizing/campaign_detail.html', context)
