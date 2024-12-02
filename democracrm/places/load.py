from pathlib import Path
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from .models import Boundary

boundary_mapping = {
    'geoid': 'GEOID',
    'geoidfq': 'GEOIDFQ',
    'namelsad': 'NAMELSAD',
    'lsy': 'LSY',
    'aland': 'ALAND',
    'awater': 'AWATER',
    'intptlat': 'INTPTLAT',
    'intptlon': 'INTPTLON',
    'geom': 'MULTIPOLYGON',
}

import_source = Path('data/imports/tlgpkg_2024_a_us_legislative.gpkg')
data_source = DataSource(import_source)
boundary_layer = data_source[1]

def run(verbose=True):
    lm = LayerMapping(Boundary, data_source, boundary_mapping, layer=1, transform=False)
    lm.save(strict=True, verbose=verbose)