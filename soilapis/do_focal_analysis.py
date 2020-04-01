"""
    Loop through each folder of 6 layers
    For each layer:
    - Convert a geotif file to array of float
    - Given a window size, create an array of average values
 -
"""

import os
from scipy import ndimage
from osgeo import gdal
import numpy as np
import time
import datetime


def convert_to_min(n):
    return str(datetime.timedelta(seconds=n))


def average(data):
    return np.mean(data)

in_fn = "/home/eusojk/Downloads/layers/soilproperties/bulkdensity/THA/tha_bds_0cm.tif"
#
in_ds = gdal.Open(in_fn)
in_data = in_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

# out_data = ndimage.filters.uniform_filter(in_data, size=3, mode='nearest')
f3 = in_data[0:20, 0:20]
then = time.time()
out_data = ndimage.filters.generic_filter( in_data, average, size=20, mode='nearest')
now = time.time()
print('done in: ', convert_to_min(now - then))
np.savetxt('out_data.out', out_data, delimiter=',', fmt='%1.0d')
print(f3)
print(np.mean(f3))
print(out_data.shape)

del in_ds

# go through each of the 4 directories: 'bulkdensity', clay, sand, organic
# initialize a dict: { bulkdensity : dict_of_bulkdensity_layers }

# for each layer in directory: e.g. bulkdensity
# (loop 6 x)
#   - initiliase the dir name into a dict: dict_of_ + [dir_name] + _layers which will contain 6 items
#   - make a layer into an array of averages based on the windowing/grid size: layer_0 for 0cm
#   - store that array into the dict: dict_of_bulkdensity_layers[layer_0] = arr































