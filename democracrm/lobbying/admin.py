from django.contrib import admin


from .models import (PoliticalParty, Voter,
                     GoverningBody, PoliticalSubdivision, PublicOfficial,
                     PublicOffice, Committee, Legislation, LegislativeSession,
                     SupportLevel, InterpersonalTie)


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


@admin.register(PublicOffice)
class PublicOfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body', 'seats', 'officials_count']


@admin.register(PoliticalSubdivision)
class PoliticalSubdivisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body', 'office', 'district', 'seats']


@admin.register(PublicOfficial)
class PublicOfficialAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'is_elected', 'is_leadership', 'party', 'role', 'subdivision']


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['name', 'body', 'office']


@admin.register(LegislativeSession)
class LegislativeSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'body', 'start_date', 'end_date']


@admin.register(Legislation)
class LegislationAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'url', 'status', 'campaign']


@admin.register(SupportLevel)
class SupportLevelAdmin(admin.ModelAdmin):
    list_display = ['official', 'campaign', 'campaign_support', 'legislation', 'legislation_support']


@admin.register(InterpersonalTie)
class InterpersonalTieAdmin(admin.ModelAdmin):
    list_display = ['official1', 'tie_strength', 'tie_affinity', 'official2']
