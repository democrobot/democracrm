import pathlib

from django.test import TestCase
from django.conf import settings

from .utils import (
    create_file,
    scrape_pa_senate_committees,
    scrape_pa_senate_members,
    scrape_pa_house_committees,
    scrape_pa_house_members,
)


class FilePathTests(TestCase):

    def test_file_creation(self):
        path = create_file()
        test_file = pathlib.Path(path)
        self.assertTrue(test_file.is_file())
        test_file.unlink()


class DataScrapingTests(TestCase):
    
    def test_scrape_pa_senate_committees(self):
        print('Testing PA Senate committees')
        scrape_pa_senate_committees()
    
    def test_scrape_pa_senate_members(self):
        print('Testing PA Senate members')
        scrape_pa_senate_members()
    
    def test_scrape_pa_house_committees(self):
        scrape_pa_house_committees()
        self.fail()
    
    def test_scrape_pa_house_members(self):
        print('Testing PA House members')
        scrape_pa_house_members()
