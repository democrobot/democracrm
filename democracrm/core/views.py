from django.shortcuts import render

from accounts.models import OrganizationAccount


def index(request):
    return render(request, 'core/index.html', {})


def organization_root(request, slug):
    org_account = OrganizationAccount.objects.get(slug=slug)
    context = {
        'org_account': org_account,
        'description': "Statewide, nonpartisan, volunteer-driven org in PA working to take democracy where it's NEVER been!",
        'hq_address': 'Philadelphia, PA',
        'website_url': 'https://www.mohpa.org',
        'email_address': 'info@mohpa.org',
        'facebook_handle': 'MarchOnHarrisburg2',
        'twitter_handle': 'endpacorruption',
        'instagram_handle': 'mohpa',
        'tiktok_handle': 'mohpa',
        'youtube_handle': 'mohpa',
        'phone_number': '215-345-6789',

    }
    return render(request, 'core/organization_root.html', context)
