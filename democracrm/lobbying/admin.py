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
    list_display = ['full_name', 'title', 'role', 'is_elected', 'is_leadership', 'leadership_title', 'political_party',
                    'political_subdivision']
    list_filter = ['is_elected', 'is_leadership', 'public_office', 'role', 'political_party']
    ordering = ['last_name', 'first_name']
    search_help_text = 'Search on last name, district, leadership title, and notes'
    search_fields = ['last_name', 'political_subdivision__district', 'leadership_title', 'notes']

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
