from django.contrib import admin


from .models import SocialMediaAccount, PoliticalParty, Voter


@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['handle', 'platform', 'url']


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    pass


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'first_name', 'last_name', 'party']
    #readonly_fields = ('uuid',)

