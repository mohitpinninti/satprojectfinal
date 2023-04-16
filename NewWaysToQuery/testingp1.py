from pystac_client import Client

#LandsatSTAC = Client.open("https://landsatlook.usgs.gov/stac-server", headers=[])

from json import load
file_path = "my-area.geojson"
file_content = load(open(file_path))
geometry = file_content["features"][0]["geometry"]

timeRange = '2019-02-27/2019-09-25'

#LandsatSearch = LandsatSTAC.search (
#    intersects = geometry,
#    datetime = timeRange,
#    query =  ['eo:cloud_cover95'],
#    collections = ["landsat-c2l2-sr"] )
#
#Landsat_items = [i.to_dict() for i in LandsatSearch.get_items()]
#print(f"{len(Landsat_items)} Landsat scenes fetched")


#for i in range(len(Landsat_items)):
#    if (i == 0):
#        print(Landsat_items[i])

import satsearch

SentinelSearch = satsearch.Search.search(
    url = "https://earth-search.aws.element84.com/v0",
    intersects = geometry,
    datetime = timeRange,
    collections = ['sentinel-s2-l2a-cogs'],
    query={"eo:cloud_cover":{"lt":5}} )

Sentinel_items = SentinelSearch.items()
print(Sentinel_items.summary())


import rioxarray

for i in range(len(Sentinel_items)):
    if (i == 0):
        #print(Sentinel_items[i].assets)
        assets = Sentinel_items[i].assets
        for key in assets.keys():
            if (str(key)[0] == "B"):
                print("starting work on band " + str(key))
                band_href = assets[key]["href"]
                band = rioxarray.open_rasterio(band_href)
                band.rio.to_raster(key + ".tif")
                print("data acquired for " + str(key))
                print("waiting for next key")
#        b01 = assets["B01"]
#        b01_href = assets["B01"]["href"]
#        b01 = rioxarray.open_rasterio(b01_href)
#        b01.rio.to_raster("B01.tif")

        #print(Sentinel_items[i].assets.keys())
        #for key, asset in Sentinel_items[i].assets.items():
        #    print(f"{key}: {asset.title}")

