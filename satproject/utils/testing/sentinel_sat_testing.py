from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from env import SENTINEL_API_USERNAME, SENTINEL_API_PASSWORD

id = '514adfb5-9456-4aff-a8ee-41bbb53141ff'
api = SentinelAPI(SENTINEL_API_USERNAME, SENTINEL_API_PASSWORD, 'https://apihub.copernicus.eu/apihub')
title = api.get_product_odata(id)['title']
print(title)