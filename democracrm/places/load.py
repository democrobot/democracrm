from pathlib import Path
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from .models import Boundary

def load_states(verbose=True):
    boundary_mapping = {
        'geoid': 'GEOID',
        'geoidfq': 'GEOIDFQ',
        'statens': 'STATENS',
        #'namelsad': 'NAMELSAD',
        'stusps': 'STUSPS',
        'name': 'NAME',
        #'lsy': 'LSY',
        'aland': 'ALAND',
        'awater': 'AWATER',
        'intptlat': 'INTPTLAT',
        'intptlon': 'INTPTLON',
        'geom': 'MULTIPOLYGON',
    }

    import_source = Path('data/imports/tlgpkg_2024_a_us_substategeo.gpkg')
    data_source = DataSource(import_source)
    lm = LayerMapping(Boundary, data_source, boundary_mapping, layer='State', transform=False)
    lm.save(strict=True, verbose=verbose)

def load_upper_chambers(verbose=True):
    boundary_mapping = {
        'geoid': 'GEOID',
        'geoidfq': 'GEOIDFQ',
        #'statens': 'STATENS',
        'namelsad': 'NAMELSAD',
        #'stusps': 'STUSPS',
        #'name': 'NAME',
        'lsy': 'LSY',
        'aland': 'ALAND',
        'awater': 'AWATER',
        'intptlat': 'INTPTLAT',
        'intptlon': 'INTPTLON',
        'geom': 'MULTIPOLYGON',
    }

    import_source = Path('data/imports/tlgpkg_2024_a_us_legislative.gpkg')
    data_source = DataSource(import_source)
    lm = LayerMapping(Boundary, data_source, boundary_mapping, layer='State_Legislative_Districts_Upper', transform=False)
    lm.save(strict=True, verbose=verbose)

def load_lower_chambers(verbose=True):
    boundary_mapping = {
        'geoid': 'GEOID',
        'geoidfq': 'GEOIDFQ',
        #'statens': 'STATENS',
        'namelsad': 'NAMELSAD',
        #'stusps': 'STUSPS',
        #'name': 'NAME',
        'lsy': 'LSY',
        'aland': 'ALAND',
        'awater': 'AWATER',
        'intptlat': 'INTPTLAT',
        'intptlon': 'INTPTLON',
        'geom': 'MULTIPOLYGON',
    }

    import_source = Path('data/imports/tlgpkg_2024_a_us_legislative.gpkg')
    data_source = DataSource(import_source)
    lm = LayerMapping(Boundary, data_source, boundary_mapping, layer='State_Legislative_Districts_Lower', transform=False)
    lm.save(strict=True, verbose=verbose)

def classify_boundaries():
    # Classify states
    states = Boundary.objects.filter(geoidfq__startswith='0400000US')
    states.update(level='state')

    # Classify upper and lower chambers
    upper_chambers = Boundary.objects.filter(geoidfq__startswith='610U900US')
    upper_chambers.update(level='upper_legislative')
    lower_chambers = Boundary.objects.filter(geoidfq__startswith='620L900US')
    lower_chambers.update(level='lower_legislative')
    
    # Classify chamber states
    

def run(verbose=True):
    print('Loading states...')
    load_states()

    print('Loading state upper chambers...')
    load_upper_chambers()

    print('Loading state lower chambers...')
    load_lower_chambers()