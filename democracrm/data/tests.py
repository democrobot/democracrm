import pathlib
import requests


from django.test import TestCase
from django.conf import settings

from .utils import (
    create_file,
    scrape_pa_senate_committees,
    scrape_pa_senate_members,
    scrape_pa_house_committees,
    scrape_pa_house_members,
)


class OpenStatesTests(TestCase):

    def test_get_pa_bulk_legislators(self):
        pass


class FilePathTests(TestCase):

    def test_cached_file_creation(self):
        test = open(settings.BASE_DIR / 'data/cached_data/test.html', 'w')
        file_path = pathlib.Path(test.name)
        test.write('<html></html>')
        test.close()
        test_file = pathlib.Path(file_path)
        self.assertTrue(test_file.is_file())
        test_file.unlink()


class DataScrapingTests(TestCase):
    
    def test_scrape_pa_senate_committees(self):
        scrape_pa_senate_committees()
    
    def test_scrape_pa_senate_members(self):
        scrape_pa_senate_members()
    
    def test_scrape_pa_house_committees(self):
        scrape_pa_house_committees()
    
    def test_scrape_pa_house_members(self):
        scrape_pa_house_members()
