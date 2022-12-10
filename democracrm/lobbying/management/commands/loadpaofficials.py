import csv
import json
from pathlib import Path

from django.contrib.gis.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from lobbying.models import (
    PoliticalParty,
    PublicOffice,
    PoliticalSubdivision,
    PublicOfficial,
)

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0

class Command(BaseCommand):
    help = 'Loads public official data into PublicOfficial records'

    def add_arguments(self, parser):
        parser.add_argument('office', nargs='+', type=str)
        parser.add_argument('data_file', nargs='+', type=str)

    def handle(self, *args, **options):

        start_time = timezone.now()
        print(options)
        office = options['office'][0]
        data_file = Path(options['data_file'][0])
        print(data_file)

        if office == 'PA State House':
            print('Loading records for PA State House')
            try:
                public_office = PublicOffice.objects.get(name='PA State House')
            except PublicOffice.DoesNotExist:
                print('Public office not found!')
            with open(data_file, "r") as csv_file:
                data = list(csv.reader(csv_file, delimiter=","))
                for row in data[1:]:
                    public_official = {}
                    public_official['district'] = int(row[1])
                    public_official['first_name'] = row[2][:-3] if '.' in row[2] else row[2]
                    public_official['middle_name'] = row[2][-2] if '.' in row[2] else ''
                    public_official['last_name'] = row[3]
                    public_official['political_party'] = row[4]
                    public_official['is_leadership'] = True if int(row[7]) == 1 else False
                    public_official['leadership_title'] = row[8]
                    public_official['official_profile_url'] = row[9]
                    public_official['official_profile_thumbnail_url'] = row[10]
                    public_official['official_profile_photo_url'] = row[11]
                    public_official['description'] = row[16]
                    public_official['is_seeking_reelection'] = True if row[17] == 'Yes' else False
                    public_official['notes'] = f"""
                        Gift Ban Support: {row[19]}
                        Dem. Challenger: {row[18]}
                        Dem. Gift Ban Support: {row[23]}
                        Rep. Challenger: {row[21]}
                        Rep. Gift Ban Support: {row[24]}
                        Other Challenger: {row[22]}
                        Other Gift Ban Support: {row[25]}
                        Re-election District: {row[27]}"""

                    PublicOfficial.objects.get_or_create(
                        first_name=public_official['first_name'],
                        middle_name=public_official['middle_name'],
                        last_name=public_official['last_name'],
                        public_office=public_office,
                        political_subdivision=PoliticalSubdivision.objects.get(
                            Q(public_office=public_office),
                            Q(district=public_official['district'])
                        ),
                        description=public_official['description'],
                        is_leadership=public_official['is_leadership'],
                        leadership_title=public_official['leadership_title'],
                        is_seeking_reelection=public_official['is_seeking_reelection'],
                        political_party=PoliticalParty.objects.get(name=public_official['political_party']),
                        official_profile_url=public_official['official_profile_url'],
                        official_profile_thumbnail_url=public_official['official_profile_thumbnail_url'],
                        official_profile_photo_url=public_official['official_profile_photo_url'],
                        notes=public_official['notes']
                    )

        elif office == 'PA State Senate':
            print('Loading records for PA State Senate')
            try:
                public_office = PublicOffice.objects.get(name='PA State Senate')
            except PublicOffice.DoesNotExist:
                print('Public office not found!')
            with open(data_file, "r") as json_file:
                data = json.load(json_file)
                for row in data:
                    senator = {}
                    senator['district'] = int(row['old_district'])
                    senator['first_name'] = row['name'][1][:-3] if '.' in row['name'][1] else row['name'][1]
                    senator['middle_name'] = row['name'][1][-2] if '.' in row['name'][1] else ''
                    senator['last_name'] = row['name'][0]
                    senator['public_office'] = public_office
                    senator['political_subdivision'] = PoliticalSubdivision.objects.get(
                        public_office=public_office,
                        district=int(row['old_district'])
                    )
                    senator['is_seeking_reelection'] = True
                    if row.get('party_affiliation', '') in ('Democratic', 'Republican'):
                        senator['political_party'] = PoliticalParty.objects.get(name=row['party_affiliation'])
                    else:
                        senator['political_party'] = PoliticalParty.objects.get(name='Independent')
                    senator['official_profile_url'] = row['bio_url']
                    senator['official_profile_thumbnail_url'] = row['photo_thumb_url']
                    senator['official_profile_photo_url'] = row['photo_url']

                    PublicOfficial.objects.get_or_create(
                        first_name=senator['first_name'],
                        middle_name=senator['middle_name'],
                        last_name=senator['last_name'],
                        public_office=senator['public_office'],
                        political_subdivision=PoliticalSubdivision.objects.get(
                            Q(public_office=senator['public_office']),
                            Q(district=senator['district'])
                        ),
                        is_seeking_reelection=senator['is_seeking_reelection'],
                        political_party=senator['political_party'],
                        official_profile_url=senator['official_profile_url'],
                        official_profile_thumbnail_url=senator['official_profile_thumbnail_url'],
                        official_profile_photo_url=senator['official_profile_photo_url'],
                    )

        else:
            print('Office not recognized.')

        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading JSON took: {(end_time - start_time).total_seconds()} seconds."))
