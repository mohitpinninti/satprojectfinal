# from env import FILE_PATH
# import utils
from utils.testing.regex_testing import find_band
#   from file_handling import find_band
import rasterio

import os
#import tensorflow_decision_forests as tfdf
from tensorflow import keras
import numpy as np


def query_model(sat_product_name):
    #import model
    model_path = os.path.join(FILE_PATH, "catname_model_GBT")
    model = keras.models.load_model(model_path)
    bands_folder = os.path.join(FILE_PATH, sat_product_name)

    #open the downloaded satellite data
    band1 = rasterio.open(find_band("B01.jp2", bands_folder)).read(1)  # coastal aerosol, 60m
    band2 = rasterio.open(find_band("B02.jp2", bands_folder)).read(1)  # blue, 10m
    band3 = rasterio.open(find_band("B03.jp2", bands_folder)).read(1)  # green, 10m
    band4 = rasterio.open(find_band("B04.jp2", bands_folder)).read(1)  # red, 10m
    band5 = rasterio.open(find_band("B05.jp2", bands_folder)).read(1)  # veg red edge, 20m
    band6 = rasterio.open(find_band("B06.jp2", bands_folder)).read(1)  # veg red edge, 20m
    band7 = rasterio.open(find_band("B07.jp2", bands_folder)).read(1)  # veg red edge, 20m
    band8 = rasterio.open(find_band("B08.jp2", bands_folder)).read(1)  # nir, 10m
    band8A = rasterio.open(find_band("B8A.jp2", bands_folder)).read(1) # veg red edge, 20m
    band9 = rasterio.open(find_band("B09.jp2", bands_folder)).read(1)  # water vapor, 60m
    band10 = rasterio.open(find_band("B10.jp2", bands_folder)).read(1) # swir cirrus, 60m
    band11 = rasterio.open(find_band("B11.jp2", bands_folder)).read(1) # swir, 20m
    band12 = rasterio.open(find_band("B12.jp2", bands_folder)).read(1) # swir, 20m

    # orig_band_array = [band1, band2, band3, band4, band5, band6, band7, band8, band8A, band9, band10, band11, band12]
    # for band in orig_band_array:
    #     print(band.shape)

    #reshape the satellite data so that all data bands match the same size
    band1_10m = np.repeat(band1, 6, axis=0)
    band1_10m = np.repeat(band1_10m, 6)
    band5_10m = np.repeat(band5, 2, axis=0)
    band5_10m = np.repeat(band5_10m, 2)
    band6_10m = np.repeat(band6, 2, axis=0)
    band6_10m = np.repeat(band6_10m, 2)
    band7_10m = np.repeat(band7, 2, axis=0)
    band7_10m = np.repeat(band7_10m, 2)
    band8A_10m = np.repeat(band8A, 2, axis=0)
    band8A_10m = np.repeat(band8A_10m, 2)
    band9_10m = np.repeat(band9, 6, axis=0)
    band9_10m = np.repeat(band9_10m, 6)
    band10_10m = np.repeat(band10, 6, axis=0)
    band10_10m = np.repeat(band10_10m, 6)
    band11_10m = np.repeat(band11, 2, axis=0)
    band11_10m = np.repeat(band11_10m, 2)
    band12_10m = np.repeat(band12, 2, axis=0)
    band12_10m = np.repeat(band12_10m, 2)

    flat_band_array = [band1_10m, band2.flatten(), band3.flatten(), band4.flatten(), band5_10m, band6_10m, 
        band7_10m, band8.flatten(), band9_10m, band10_10m, band11_10m, band12_10m]
    
    # for band in flat_band_array:
    #     print(band.shape)

    #format the data into a numpy array for prediction
    flattened_size = flat_band_array[0].shape[0]
    predict_on = np.zeros((flattened_size, 12))
    for index in range(flattened_size):
        for band_num, band in enumerate(flat_band_array):
            predict_on[index][band_num] = band[index]

    # print(predict_on)
    # print(predict_on.shape)

    predictions = model.predict(predict_on, batch_size=1000, use_multiprocessing=True)
    return predictions


#query_model()