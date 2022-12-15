from django.shortcuts import render

from .models import PublicOfficial, SupportLevel


def index(request):
    return render(request, 'lobbying/index.html', {})


def officials_directory(request):
    public_officials = PublicOfficial.objects.all()
    house_officials = PublicOfficial.objects.filter()
    context = {'public_officials': public_officials}
    return render(request, 'lobbying/public_officials.html', context=context)


def official_profile(request, official_id):
    public_official = PublicOfficial.objects.get(id=official_id)
    support_levels = SupportLevel.objects.filter(public_official=official_id)
    context = {'public_official': public_official, 'support_levels': support_levels}
    return render(request, 'lobbying/public_official_profile.html', context=context)
