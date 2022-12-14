import csv
import json
from pathlib import Path
from dateutil.parser import parse

from django.contrib.gis.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from lobbying.models import PoliticalParty, Voter
from places.models import Boundary

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0

class Command(BaseCommand):
    help = 'Loads voter data into Voter records'

    def add_arguments(self, parser):
        parser.add_argument('data_file', nargs='+', type=str)

    def handle(self, *args, **options):

        start_time = timezone.now()
        print(options)
        data_file = Path(options['data_file'][0])
        print(data_file)

        print('Loading records for PA Voters')
        try:
            pennsylvania = Boundary.objects.get(name='Pennsylvania', level='state')
        except Boundary.DoesNotExist:
            print('Boundary not found!')
        with open(data_file, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter="\t"))
            for row in data:
                voter = {}

                voter['id'] = row[0]
                voter['prefix_name'] = row[1]
                voter['last_name'] = row[2]
                voter['first_name'] = row[3]
                voter['middle_name'] = row[4]
                voter['suffix_name'] = row[5]
                voter['sex'] = row[6]
                voter['birth_date'] = parse(row[7]).date().isoformat()
                voter['initial_registration_date'] = parse(row[8]).date().isoformat()
                print(row[9])
                if row[9] == 'A':
                    voter['status'] = Voter.Status.ACTIVE
                elif row[9] == 'IA':
                    voter['status'] = Voter.Status.INACTIVE
                voter['last_registration_date'] = parse(row[10]).date().isoformat()
                if row[11] == 'D':
                    voter['political_party'] = PoliticalParty.objects.get(name='Democratic')
                elif row[11] == 'R':
                    voter['political_party'] = PoliticalParty.objects.get(name='Republican')
                elif row[11] == 'LN':
                    voter['political_party'] = PoliticalParty.objects.get(name='Libertarian')
                elif row[11] == 'GR':
                    voter['political_party'] = PoliticalParty.objects.get(name='Green')
                elif row[11] == 'I':
                    voter['political_party'] = PoliticalParty.objects.get(name='Independent')
                elif row[11] in ('NON', 'NF'):
                    voter['political_party'] = PoliticalParty.objects.get(name='Non-Affiliated')
                else:
                    voter['political_party'] = 'Other'
                voter['physical_address_street_number'] = row[12]
                voter['physical_address_street_number_suffix'] = row[13]
                voter['physical_address_street_name'] = row[14]
                voter['physical_address_unit'] = row[15]
                voter['physical_address_supplemental'] = row[16]
                voter['physical_address_city'] = row[17]
                voter['state'] = Boundary.objects.get(name='Pennsylvania', level='state')
                voter['physical_address_zip_code'] = row[19]
                #voter['mailing_address'] = row[20]
                #voter['mailing_address_supplemental'] = row[21]
                #voter['mailing_address_city'] = row[22]
                #voter['mailing_address_state'] = row[23]
                #voter['mailing_address_zip_code'] = row[24]
                #voter['last_election_date'] = row[25]
                #voter['voter_precinct'] = row[26]
                #voter['voter_polling_place'] = row[27]
                #voter['last_voting_date'] = row[28]
                voter['phone_number'] = row[-3]
                voter['county'] = Boundary.objects.get(name='Berks', level='county')
                #voter['data_export_date'] = '10/04/2022'
                print(voter)

                Voter.objects.get_or_create(
                    id=voter.pop('id'),
                    defaults=voter
                )

        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading JSON took: {(end_time - start_time).total_seconds()} seconds."))
