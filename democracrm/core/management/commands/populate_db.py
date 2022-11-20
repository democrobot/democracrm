from django.core.management.base import BaseCommand, CommandError

from accounts.models import User, Organization
from core.models import GeographicBoundary
#from lobbying.models import *
from organizing.models import Platform, PlatformCategory, Campaign


class Command(BaseCommand):
    help = 'Populates database with test data'

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS(f'Created user account'))

        area = GeographicBoundary(name='Pennsylvania')
        area.save()
        self.stdout.write(self.style.SUCCESS(f'Created boundaries'))

        organization = Organization(name='March on Harrisburg', territory=area)
        organization.save()
        self.stdout.write(self.style.SUCCESS(f'Created organization account'))

        platform = Platform(name='Official Platform')
        self.stdout.write(self.style.SUCCESS(f'Created platform'))
