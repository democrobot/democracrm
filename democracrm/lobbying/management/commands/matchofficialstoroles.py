from django.core.management.base import BaseCommand, CommandError
from lobbying.models import (
    PublicOfficial,
    PublicOfficialRole
)


class Command(BaseCommand):
    help = 'Match public official data into PublicOfficialRole records'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for public_official in PublicOfficial.objects.filter(is_elected=True):
            for public_official_role in PublicOfficialRole.objects.all():
                if public_official.political_subdivision == public_official_role.political_subdivision:
                    print(f'{public_official} -> {public_official_role}')
                    public_official_role.public_official = public_official
                    public_official_role.is_leadership = public_official.is_leadership
                    public_official_role.leadership_title = public_official.leadership_title
                    public_official_role.official_profile_url = public_official.official_profile_url
                    public_official_role.official_profile_thumbnail_url = public_official.official_profile_thumbnail_url
                    public_official_role.official_profile_photo_url = public_official.official_profile_photo_url
                    public_official_role.save()

        self.stdout.write(self.style.SUCCESS('Success!'))