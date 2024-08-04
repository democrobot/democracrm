import django
import pathlib
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from django.conf import settings


urls = {
    'pa_senate_committees': {
        'web': 'https://www.palegis.us/senate/committees/committee-list',
        'local': 'data/cached_data/pa_senate_committees.html'
    },
    'pa_senate_members': {
        'web': 'https://www.palegis.us/senate/members',
        'local': 'data/cached_data/pa_senate_members.html'
    },
    'pa_house_committees': {
        'web': 'https://www.palegis.us/house/committees/committee-list',
        'local': 'data/cached_data/pa_house_committees.html'
    },
    'pa_house_members': {
        'web': 'https://www.palegis.us/house/members',
        'local': 'data/cached_data/pa_house_members.html'
    }
}

def create_file():
    test = open(settings.BASE_DIR / 'data/cached_data/test.html', 'w')
    file_path = pathlib.Path(test.name)
    test.write('<html></html>')
    test.close()
    return file_path


def scrape_pa_senate_committees():

    # Scrape committee data
    # Caching to address rate limiting

    pa_senate_committees_file = pathlib.Path(settings.BASE_DIR / urls['pa_senate_committees']['local'])

    if pa_senate_committees_file.is_file() and \
        datetime.fromtimestamp(pa_senate_committees_file.stat().st_mtime).date() == datetime.now().date():
        print('Using PA Senate Committee cached data')
        page = open(pa_senate_committees_file, 'r').read()
    else:
        print('Using PA Senate Committee web data')
        response = requests.get(urls['pa_senate_committees']['web'])
        print(response.status_code)
        page = response.text
        cached_page = open(pa_senate_committees_file, 'w')
        cached_page.write(page)
        cached_page.close()
    
    soup = BeautifulSoup(page, 'html.parser')
    committee_list = soup.find('div', class_='committee-list')
    
    print(f'PA Senate Committees: found {len(committee_list) or 0} results')

def scrape_pa_senate_members():

    # Scrape member data
    # - Get leadership assignments
    # - Get committee assignments

    pa_senate_members_file = pathlib.Path(settings.BASE_DIR / urls['pa_senate_members']['local'])

    if pa_senate_members_file.is_file() and \
        datetime.fromtimestamp(pa_senate_members_file.stat().st_mtime).date() == datetime.now().date():
        print('Using PA Senate Members cached data')
        page = open(pa_senate_members_file, 'r').read()
    else:
        print('Using PA Senate Members web data')
        page = requests.get(urls['pa_senate_members']['web']).text
        cached_page = open(pa_senate_members_file, 'w')
        cached_page.write(page)
        cached_page.close()
        
    soup = BeautifulSoup(page, 'html.parser')
    member_list = soup.find_all('div', class_='member')
        
    print(f'PA Senate Members: found {len(member_list)} results')

def scrape_pa_house_committees():
    # Scrape committee data
    # Caching to address rate limiting

    pa_house_committees_file = pathlib.Path(settings.BASE_DIR / urls['pa_house_committees']['local'])

    if pa_house_committees_file.is_file() and \
        datetime.fromtimestamp(pa_house_committees_file.stat().st_mtime).date() == datetime.now().date():
        print('Using PA House Committee cached data')
        page = open(pa_house_committees_file, 'r').read()
    else:
        print('Using PA House Committee web data')
        response = requests.get(urls['pa_house_committees']['web'])
        print(response.status_code)
        page = response.text
        cached_page = open(pa_house_committees_file, 'w')
        cached_page.write(page)
        cached_page.close()
    
    soup = BeautifulSoup(page, 'html.parser')
    committee_list = soup.find('div', class_='committee-list')
    
    print(f'PA House Committees: found {len(committee_list) or 0} results')

def scrape_pa_house_members():
    # Scrape member data
    # - Get leadership assignments
    # - Get committee assignments

    pa_house_members_file = pathlib.Path(settings.BASE_DIR / urls['pa_house_members']['local'])

    if pa_house_members_file.is_file() and \
        datetime.fromtimestamp(pa_house_members_file.stat().st_mtime).date() == datetime.now().date():
        print('Using PA House Members cached data')
        page = open(pa_house_members_file, 'r').read()
    else:
        print('Using PA House Members web data')
        response = requests.get(urls['pa_house_members']['web'])
        print(response.status_code)
        page = response.text
        cached_page = open(pa_house_members_file, 'w')
        cached_page.write(page)
        cached_page.close()
        
    soup = BeautifulSoup(page, 'html.parser')
    member_list = soup.find_all('div', class_='member')
        
    print(f'PA House Members: found {len(member_list)} results')
