from django.core.management.base import BaseCommand, CommandError
from lobbying.models import (
    PoliticalParty,
    GoverningBody,
    PublicOffice,
    PoliticalSubdivision,
    PublicOfficial,
    PublicOfficialPosition
)
from places.models import Boundary


class Command(BaseCommand):
    help = 'Loads initial PA boundaries, gov. bodies, public official data into PublicOfficial records'

    def add_arguments(self, parser):
        pass

    @staticmethod
    def create_subdivisions_roles(public_office, boundary):

        if public_office.total_seats == 1:
            political_subdivision, created = PoliticalSubdivision.objects.get_or_create(
                boundary=boundary,
                public_office=public_office,
                name=public_office.name,
                seats=public_office.total_seats
            )
            public_official_position, created = PublicOfficialPosition.objects.get_or_create(
                office_type=PublicOfficialPosition.Type.EXECUTIVE,
                public_office=public_office,
                name=public_office.name,
                political_subdivision=political_subdivision
            )
            print(f'{political_subdivision} and {public_official_position} created or updated')
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
                public_official_position, created = PublicOfficialPosition.objects.get_or_create(
                    office_type=PublicOfficialPosition.Type.LEGISLATIVE,
                    public_office=public_office,
                    name=f'District {seat} {chamber_role}',
                    political_subdivision=political_subdivision
                )
                print(f'{political_subdivision} and {public_official_position} created or updated')

    def handle(self, *args, **options):
        print('Updating Pennsylvania state data')

        nation_boundary, created = Boundary.objects.get_or_create(
            name='United States',
            level='nation'
        )

        state_boundary, created = Boundary.objects.get_or_create(
            name='Pennsylvania',
            level='state',
            parent=nation_boundary
        )

        governing_body, created = GoverningBody.objects.get_or_create(
            name='Pennsylvania State Government',
            level='state',
            description='Test???',
            boundary=state_boundary
        )

        state_governor, created = PublicOffice.objects.get_or_create(
            governing_body=governing_body,
            office_type='executive',
            name='PA Governor',
            total_seats=1,
            seats_per_subdivision=1
        )
        if created:
            self.create_subdivisions_roles(state_governor, state_boundary)
        else:
            print('Exists')

        state_lt_governor, created = PublicOffice.objects.get_or_create(
            governing_body=governing_body,
            office_type='executive',
            name='PA Lieutenant Governor',
            total_seats=1,
            seats_per_subdivision=1
        )
        self.create_subdivisions_roles(state_lt_governor, state_boundary)

        # # TODO: Other cabinet officers

        # state_senate, created = PublicOffice.objects.get_or_create(
        #     governing_body=governing_body,
        #     office_type='legislative',
        #     name='PA State Senate',
        #     total_seats=50,
        #     seats_per_subdivision=1
        # )
        # self.create_subdivisions_roles(state_senate)

        # state_house, created = PublicOffice.objects.get_or_create(
        #     governing_body=governing_body,
        #     office_type='legislative',
        #     name='PA State House',
        #     total_seats=203,
        #     seats_per_subdivision=1
        # )
        # self.create_subdivisions_roles(state_house)

        self.stdout.write(self.style.SUCCESS('PA Created'))