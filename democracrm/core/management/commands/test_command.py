from django.core.management.base import BaseCommand, CommandError

from accounts.models import Organization


class Command(BaseCommand):
    help = 'Experimental management command'

    def handle(self, *args, **options):
        o = Organization.objects.get(id=1)
        self.stdout.write(self.style.SUCCESS(f'{o}'))
