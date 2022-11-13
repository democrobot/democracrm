from django.contrib import admin


from .models import (SocialMediaAccount, PoliticalParty, Voter,
                     GoverningBody, PoliticalSubdivision, PublicOfficial,
                     PublicOffice)


@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['handle', 'platform', 'url']


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    pass


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'first_name', 'last_name', 'party', 'uuid']
    readonly_fields = ('uuid',)


@admin.register(GoverningBody)
class GoverningBodyAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']


@admin.register(PoliticalSubdivision)
class PoliticalSubdivisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'office']


@admin.register(PublicOffice)
class PublicOfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body']


@admin.register(PublicOfficial)
class PublicOfficialAdmin(admin.ModelAdmin):
    pass
