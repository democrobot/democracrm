from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from lobbying.models import (
    PoliticalParty,
    PublicOffice,
    PoliticalSubdivision,
    PublicOfficial,
)

democrat, created = PoliticalParty.objects.get_or_create(
    name='Democratic'
)
republican, created = PoliticalParty.objects.get_or_create(
    name='Republican'
)
independent, created = PoliticalParty.objects.get_or_create(
    name='Independent'
)


class Command(BaseCommand):
    help = 'Loads public official data into PublicOfficial records'

    def add_arguments(self, parser):
        parser.add_argument('office', nargs='+', type=str)
        parser.add_argument('data_file', nargs='+', type=str)

    def handle(self, *args, **options):
        print(options)
        office = options['office'][0]
        data = Path(options['data_file'][0])
        print(data)

        if office == 'State House':
            print('Loading records for PA State House')
            try:
                public_office = PublicOffice.objects.get(name='PA State House')
            except PublicOffice.DoesNotExist:
                print('Public office not found!')

        elif office == 'State Senate':
            print('Loading records for PA State Senate')
        else:
            print('Office not recognized.')

        # self.stdout.write(self.style.SUCCESS('Successfully printed "%s"' % public_office))
