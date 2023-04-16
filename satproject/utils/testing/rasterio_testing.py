from env import FILE_PATH
from find_band import find_band
import rasterio

band1 = rasterio.open(find_band("B01.jp2", FILE_PATH)).read(1)
band2 = rasterio.open(find_band("B02.jp2", FILE_PATH)).read(1)
band3 = rasterio.open(find_band("B03.jp2", FILE_PATH)).read(1)
band4 = rasterio.open(find_band("B04.jp2", FILE_PATH)).read(1)
band5 = rasterio.open(find_band("B05.jp2", FILE_PATH)).read(1)
band6 = rasterio.open(find_band("B06.jp2", FILE_PATH)).read(1)
band7 = rasterio.open(find_band("B07.jp2", FILE_PATH)).read(1)
band8 = rasterio.open(find_band("B08.jp2", FILE_PATH)).read(1)
band8A = rasterio.open(find_band("B8A.jp2", FILE_PATH)).read(1)
band9 = rasterio.open(find_band("B09.jp2", FILE_PATH)).read(1)
band10 = rasterio.open(find_band("B10.jp2", FILE_PATH)).read(1)
band11 = rasterio.open(find_band("B11.jp2", FILE_PATH)).read(1)
band12 = rasterio.open(find_band("B12.jp2", FILE_PATH)).read(1)

band_array = [band1, band2, band3, band4, band5, band6, band7, band8, band8A, band9, band10, band11, band12]

for band in band_array:
    #print(band.shape)
























# taken from here: http://step.esa.int/docs/tutorials/Performing%20SAR%20processing%20in%20Python%20using%20snappy.pdf

# import snappy
# from snappy import Product
# from snappy import ProductIO
# from snappy import ProductUtils
# from snappy import WKTReader
# from snappy import HashMap
# from snappy import GPF


# path_to_sentinel_data = "C:\\Users\\pinni\\OneDrive\\Desktop\\ADM\\satprojectFromTweetSent\\S2A_MSIL1C_20151125T163622_N0204_R083_T16SGJ_20151125T163709.zip"
# product = ProductIO.readProduct(path_to_sentinel_data)

