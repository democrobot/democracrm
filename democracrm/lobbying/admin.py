from django.contrib import admin


from .models import (PoliticalParty, Voter,
                     GoverningBody, PoliticalSubdivision, PublicOfficial,
                     PublicOffice, Committee, Legislation, LegislativeSession,
                     SupportLevel, InterpersonalTie)


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'initial']


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'first_name', 'last_name', 'political_party', 'uuid']
    readonly_fields = ('uuid',)


@admin.register(GoverningBody)
class GoverningBodyAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']


@admin.register(PublicOffice)
class PublicOfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body', 'total_seats', 'seats_per_subdivision', 'officials_count']


@admin.register(PoliticalSubdivision)
class PoliticalSubdivisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body', 'public_office', 'district', 'seats']


@admin.register(PublicOfficial)
class PublicOfficialAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'title', 'is_elected', 'is_leadership', 'political_party', 'role', 'political_subdivision']


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body', 'public_office']


@admin.register(LegislativeSession)
class LegislativeSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body', 'start_date', 'end_date']


@admin.register(Legislation)
class LegislationAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'url', 'status']


@admin.register(SupportLevel)
class SupportLevelAdmin(admin.ModelAdmin):
    list_display = ['public_official', 'campaign_support', 'legislation', 'legislation_support']


@admin.register(InterpersonalTie)
class InterpersonalTieAdmin(admin.ModelAdmin):
    list_display = ['public_official1', 'tie_strength', 'tie_affinity', 'public_official2']
