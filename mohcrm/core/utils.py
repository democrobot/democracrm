from geocodio import GeocodioClient


from mohcrm.settings import SECRETS

geocoder = GeocodioClient(SECRETS['GEOCODIO_KEY'])


def geocode_address(input_address):
    geocoded_address = geocoder.geocode(input_address)
    return geocoded_address
