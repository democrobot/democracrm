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


def run(verbose=True):
    load_states()
    load_upper_chambers()
    load_lower_chambers()