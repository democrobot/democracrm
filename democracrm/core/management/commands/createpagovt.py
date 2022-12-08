from django.core.management.base import BaseCommand, CommandError
from lobbying.models import (
    PoliticalParty,
    GoverningBody,
    PublicOffice,
    PoliticalSubdivision,
    PublicOfficial,
)
from places.models import Boundary


class Command(BaseCommand):
    help = 'Loads public official data into PublicOfficial records'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('office', nargs='+', type=str)

    def create_subdivisions(self, public_office):

        if public_office.seats == 1:
            PoliticalSubdivision.objects.get_or_create(
                office=public_office,
                name=public_office.name,
                seats=public_office.seats
            )
        else:
            # For now assume all seats are single-member districts
            # TODO: Add district seat size in PublicOffice
            for seat in range(1, public_office.seats+1):
                PoliticalSubdivision.objects.get_or_create(
                    office=public_office,
                    name=f'{public_office.name} District {seat}',
                    seats=1
                )

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
            seats=1
        )
        self.create_subdivisions(state_governor)

        state_senate, created = PublicOffice.objects.get_or_create(
            governing_body=governing_body,
            type='legislative',
            name='PA State Senate',
            seats=50
        )
        self.create_subdivisions(state_senate)

        state_house, created = PublicOffice.objects.get_or_create(
            governing_body=governing_body,
            type='legislative',
            name='PA State House',
            seats=203
        )
        self.create_subdivisions(state_house)

        self.stdout.write(self.style.SUCCESS('PA Created'))