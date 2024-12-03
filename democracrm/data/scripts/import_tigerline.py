from pathlib import Path

from django.contrib.gis.gdal import DataSource

db = Path('imports/tlgpkg_2024_a_us_legislative.gpkg')
ds = DataSource(db)

print(ds)
print(len(ds))
for layer in ds:
    print(f'Layer name: {layer}')
    print(f'Layer SRS: {layer.srs}')
    print(f'Layer Geom: {layer.geom_type}')
    print(f'Layer fields: {layer.fields}')
    print(f'Layer features: {len(layer)}')
