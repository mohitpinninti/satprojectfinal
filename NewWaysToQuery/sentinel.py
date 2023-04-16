
###################################
### Part I: Connect to STAC Servers
###################################

from pystac_client import Client

LandsatSTAC = Client.open("https://landsatlook.usgs.gov/stac-server", headers=[])

from json import load
file_path = "my-area.geojson"
file_content = load(open(file_path))
geometry = file_content["features"][0]["geometry"]

timeRange = '2019-02-27/2019-09-25'

LandsatSearch = LandsatSTAC.search ( 
    intersects = geometry,
    datetime = timeRange,
    query =  ['eo:cloud_cover95'],
    collections = ["landsat-c2l2-sr"] )

Landsat_items = [i.to_dict() for i in LandsatSearch.get_items()]
print(f"{len(Landsat_items)} Landsat scenes fetched")



import satsearch

SentinelSearch = satsearch.Search.search( 
    url = "https://earth-search.aws.element84.com/v0",
    intersects = geometry,
    datetime = timeRange,
    collections = ['sentinel-s2-l2a-cogs'],
    query={"eo:cloud_cover":{"lt":5}} )

Sentinel_items = SentinelSearch.items()
print(Sentinel_items.summary())


###################################
### Part II: Get data from AWS S3
###################################

import os
import boto3
import rasterio as rio
from pyproj import Transformer

# os.environ['CURL_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

print("Creating AWS Session")
aws_session = rio.session.AWSSession(boto3.Session(), requester_pays=True)


def getSubset(geotiff_file, bbox):
    with rio.Env(aws_session):
        with rio.open(geotiff_file) as geo_fp:
            # Calculate pixels with PyProj 
            Transf = Transformer.from_crs("epsg:4326", geo_fp.crs) 
            lat_north, lon_west = Transf.transform(bbox[3], bbox[0])
            lat_south, lon_east = Transf.transform(bbox[1], bbox[2]) 
            x_top, y_top = geo_fp.index( lat_north, lon_west )
            x_bottom, y_bottom = geo_fp.index( lat_south, lon_east )
            # Define window in RasterIO
            window = rio.windows.Window.from_slices( ( x_top, x_bottom ), ( y_top, y_bottom ) )                
            # Actual HTTP range request
            subset = geo_fp.read(1, window=window)
    return subset


from rasterio.features import bounds
import matplotlib.pyplot as plt

bbox = bounds(geometry)

def plotNDVI(nir,red,filename):
    ndvi = (nir-red)/(nir+red)
    ndvi[ndvi>1] = 1
    plt.imshow(ndvi)
    plt.savefig(filename)
    plt.close()

# import cv2

# for i,item in enumerate(Sentinel_items):
#     if (i < 1):
#         red_s3 = item.assets['B04']['href']
#         nir_s3 = item.assets['B08']['href']
#         date = item.properties['datetime'][0:10]
#         print("Sentinel item number " + str(i) + "/" + str(len(Sentinel_items)) + " " + date)
#         red = getSubset(red_s3, bbox)
#         nir = getSubset(nir_s3, bbox)
#         plotNDVI(nir,red,"sentinel/" + date + "_ndvi.png")
        # # plt.plot("sentinel/" + date + "_ndvi.png")
        # # plt.show()
        # cv2.imread("sentinel/" + date + "_ndvi.png")
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


for i,item in enumerate(Landsat_items):
    try:
        red_s3 = item['assets']['red']['alternate']['s3']['href']
        nir_s3 = item['assets']['nir08']['alternate']['s3']['href']
        date = item['properties']['datetime'][0:10]
        print("Landsat item number " + str(i) + "/" + str(len(Landsat_items)) + " " + date)
        red = getSubset(red_s3, bbox)
        nir = getSubset(nir_s3, bbox)
        plotNDVI(nir,red,"landsat/" + date + "_ndvi.png")
    except:
        print("Issue with - Landsat item number " + str(i) + "/" + str(len(Landsat_items)) + " " + date)
    
# import cv2
# read image 
# image = cv2.imread('path to your image')
# # show the image, provide window name first
# cv2.imshow('image window', image)
# # add wait key. window waits until user presses a key
# cv2.waitKey(0)
# # and finally destroy/close all open windows
# cv2.destroyAllWindows()
