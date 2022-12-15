from django.contrib.gis.db.models import Q
from django.shortcuts import render

from .models import Campaign
from lobbying.models import PublicOffice, PublicOfficial, SupportLevel


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
    state_house = PublicOffice.objects.get(name='PA State House')
    state_senate = PublicOffice.objects.get(name='PA State Senate')
    state_governor = PublicOffice.objects.get(name='PA Governor')
    print(state_governor)
    house_needed = 102
    senate_needed = 51
    governor_needed = 1
    supporters = campaign.supportlevel_set.filter(campaign_support=SupportLevel.Status.SUPPORTS)
    house_supporters = supporters.filter(public_official__public_office=state_house)
    governor_supporters = supporters.filter(public_official__public_office=state_governor)
    opponents = campaign.supportlevel_set.filter(campaign_support=SupportLevel.Status.OPPOSES)
    house_opponents = opponents.filter(public_official__public_office=state_house)
    governor_opponents = opponents.filter(public_official__public_office=state_governor)
    undecided = campaign.supportlevel_set.filter(campaign_support=SupportLevel.Status.UNDECIDED_ON)
    house_goal = house_needed - house_supporters.count()
    governor_goal = governor_needed - governor_supporters.count()
    context = {
        'campaign': campaign,
        'supporters': supporters,
        'house_supporters': house_supporters,
        'governor_supporters': governor_supporters,
        'opponents': opponents,
        'house_opponents': house_opponents,
        'governor_opponents': governor_opponents,
        'undecided': undecided,
        'house_goal': house_goal,
        'governor_goal': governor_goal
    }
    return render(request, 'organizing/campaign_detail.html', context)
