from django.contrib import admin


from .models import (
    PoliticalParty, Voter,
    GoverningBody, PoliticalSubdivision, PublicOfficial, PublicOfficialPosition, PublicOfficialGroup,
    PublicOffice, Committee, Legislation, LegislationGroup, LegislativeSession,
    SupportLevel, InterpersonalTie
)


@admin.register(PoliticalParty)
class PoliticalPartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'initial']


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'id', 'status', 'political_party', 'full_physical_address',
                    'county', 'email_address', 'phone_number']
    readonly_fields = ('uuid',)


@admin.register(GoverningBody)
class GoverningBodyAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']


@admin.register(PublicOffice)
class PublicOfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'office_type', 'parent', 'governing_body', 'total_seats', 'officials_count']


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


@admin.register(PublicOfficialPosition)
class PublicOfficialPositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'public_official', 'public_office', 'is_leadership', 'leadership_title', 'political_party', 'political_subdivision']
    list_filter = ['is_elected', 'is_leadership', 'public_office', 'public_official__political_party']
    #ordering = ['last_name', 'first_name']
    search_help_text = 'Search on last name, district, leadership title, and notes'
    search_fields = ['public_official__last_name', 'political_subdivision__district', 'leadership_title', 'notes']

    @admin.display(description='Political Party')
    def political_party(self, obj):
        if obj.public_official.political_party:
            return obj.public_official.political_party
        else:
            return None


@admin.register(PublicOfficialGroup)
class PublicOfficialGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body', 'public_office']


@admin.register(LegislativeSession)
class LegislativeSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'governing_body', 'start_date', 'end_date']


@admin.register(Legislation)
class LegislationAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'url', 'status']


@admin.register(LegislationGroup)
class LegislationGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(SupportLevel)
class SupportLevelAdmin(admin.ModelAdmin):
    list_display = ['public_official', 'campaign_support', 'legislation_support']
    list_filter = ['public_official', 'campaign_support', 'legislation_support', 'public_official__is_leadership', 'public_official__public_office', 'public_official__political_party']
    # ordering = ['last_name', 'first_name']
    # search_help_text = 'Search on last name, district, leadership title, and notes'
    search_fields = ['public_official__first_name', 'public_official__last_name', 'notes']

@admin.register(InterpersonalTie)
class InterpersonalTieAdmin(admin.ModelAdmin):
    list_display = ['public_official1', 'tie_strength', 'tie_affinity', 'public_official2']
