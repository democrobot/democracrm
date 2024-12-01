from pathlib import Path

from django.contrib.gis.gdal import DataSource

db = Path('imports/tlgpkg_2024_a_us_legislative.gpkg')
ds = DataSource(db)

print(ds)
print(len(ds))
for layer in ds:
    print(f'{layer}: {layer.srs}, {layer.geomtype}, {len(layer)}')