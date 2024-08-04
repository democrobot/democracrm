""" Simple check that state website is up and responding"""

import requests

def site_responding(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False