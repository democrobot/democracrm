import json
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.http import JsonResponse

# from accounts.models import OrganizationAccount
from places.models import Boundary

def index(request):
    return render(request, 'core/index.html', {})

def us_index(request):
    states = Boundary.objects.filter(level='state')
    return render(request, 'core/us_index.html', {'states': states})

def us_us_geojson(request):
    geojson = serialize('geojson', Boundary.objects.filter(level='state'))
    return JsonResponse(json.loads(geojson), safe=False)

def us_pa_index(request):
    pa_state = Boundary.objects.filter(name='Pennsylvania').first()
    pa_boundaries = Boundary.objects.filter(parent=pa_state)
    pa_senate = pa_boundaries.filter(geoidfq__startswith='610U900US42')
    pa_house = pa_boundaries.filter(geoidfq__startswith='620L900US42')
    centroid = pa_state.geom.centroid.coords
    return render(request, 'core/us_pa_index.html', {'pa_senate': pa_senate, 'pa_house': pa_house,
                                                     'pa_geojson': pa_state.geom.geojson,
                                                     'centroid': centroid})

def us_pa_geojson(request):
    geojson = serialize('geojson', Boundary.objects.filter(name='Pennsylvania'))
    return JsonResponse(json.loads(geojson), safe=False)

# def organization_root(request, slug):
#     if slug:
#         org_account = OrganizationAccount.objects.get(slug=slug)
#         context = {
#             'org_account': org_account,
#             'description': "Statewide, nonpartisan, volunteer-driven org in PA working to take democracy where it's NEVER been!",
#             'hq_address': 'Philadelphia, PA',
#             'website_url': 'https://www.mohpa.org',
#             'email_address': 'info@mohpa.org',
#             'facebook_handle': 'MarchOnHarrisburg2',
#             'twitter_handle': 'endpacorruption',
#             'instagram_handle': 'mohpa',
#             'tiktok_handle': 'mohpa',
#             'youtube_handle': 'mohpa',
#             'phone_number': '215-345-6789',

#         }
#         return render(request, 'core/organization_root.html', context)
#     else:
#         pass
