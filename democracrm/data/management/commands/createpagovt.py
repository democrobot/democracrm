from django.core.management.base import BaseCommand, CommandError
from lobbying.models import (
    PoliticalParty,
    GoverningBody,
    PublicOffice,
    PoliticalSubdivision,
    PublicOfficial,
    PublicOfficialRole
)
from places.models import Boundary


class Command(BaseCommand):
    help = 'Loads public official data into PublicOfficial records'

    def add_arguments(self, parser):
        pass

    @staticmethod
    def create_subdivisions_roles(public_office):

        if public_office.total_seats == 1:
            political_subdivision, created = PoliticalSubdivision.objects.get_or_create(
                public_office=public_office,
                name=public_office.name,
                seats=public_office.total_seats
            )
            public_official_role, created = PublicOfficialRole.objects.get_or_create(
                type=PublicOfficialRole.Type.EXECUTIVE,
                public_office=public_office,
                name=public_office.name,
                political_subdivision=political_subdivision
            )
            print(f'{political_subdivision} and {public_official_role} created or updated')
        else:
            if 'House' in public_office.name:
                chamber_role = 'State Representative'
            elif 'Senate' in public_office.name:
                chamber_role = 'State Senator'
            else:
                chamber_role = 'Unknown Role'
            for seat in range(1, public_office.total_seats + 1):
                political_subdivision, created = PoliticalSubdivision.objects.get_or_create(
                    public_office=public_office,
                    name=f'{public_office.name} District {seat}',
                    district=seat,
                    seats=public_office.seats_per_subdivision
                )
                public_official_role, created = PublicOfficialRole.objects.get_or_create(
                    public_office=public_office,
                    name=f'District {seat} {chamber_role}',
                    political_subdivision=political_subdivision
                )
                print(f'{political_subdivision} and {public_official_role} created or updated')

    def handle(self, *args, **options):
        print('Creating Pennsylvania data')

        state_boundary, created = Boundary.objects.get_or_create(
            name='Pennsylvania',
            level='state'
        )

        governing_body, created = GoverningBody.objects.get_or_create(
            name='PA State Government',
            level='state',
            boundary=state_boundary
        )

        state_governor, created = PublicOffice.objects.get_or_create(
            governing_body=governing_body,
            type='executive',
            name='PA Governor',
            total_seats=1,
            seats_per_subdivision=1
        )
        self.create_subdivisions_roles(state_governor)

        state_lt_governor, created = PublicOffice.objects.get_or_create(
            governing_body=governing_body,
            type='executive',
            name='PA Lieutenant Governor',
            total_seats=1,
            seats_per_subdivision=1
        )
        self.create_subdivisions_roles(state_lt_governor)

        state_senate, created = PublicOffice.objects.get_or_create(
            governing_body=governing_body,
            type='legislative',
            name='PA State Senate',
            total_seats=50,
            seats_per_subdivision=1
        )
        self.create_subdivisions_roles(state_senate)

        state_house, created = PublicOffice.objects.get_or_create(
            governing_body=governing_body,
            type='legislative',
            name='PA State House',
            total_seats=203,
            seats_per_subdivision=1
        )
        self.create_subdivisions_roles(state_house)

        self.stdout.write(self.style.SUCCESS('PA Created'))