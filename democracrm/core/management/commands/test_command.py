from django.core.management.base import BaseCommand, CommandError

from accounts.models import OrganizationAccount


class Command(BaseCommand):
    help = 'Experimental management command'

    def handle(self, *args, **options):
        o = OrganizationAccount.objects.get(id=1)
        self.stdout.write(self.style.SUCCESS(f'{o}'))
