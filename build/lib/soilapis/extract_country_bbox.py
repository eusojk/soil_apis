"""
    This script creates a sub map of a country clipped from globe data file
"""
import argparse
import glob
import os
import sys
from pathlib import Path

import gdal
import pycountry
from country_bounding_boxes import country_subunits_by_iso_code
# from summary_soil_property import get_globe_dir
from soilapis.summary_soil_property import get_globe_dir

# Paths
script_dir = os.getcwd()
outputs = ''
parent_dir = ""
layers_dir = ""
country_dir = ""
globe_dir = ""
soilp_dir = ""
bds_dir = ""
cla_dir = ""
org_dir = ""
san_dir = ""
dir_types = ""

# Country vars
country_iso = ''
country_bbox = (0, 0, 0, 0)


def clip_by_bbox(tif_obj, bbox_tup):
    """

    :param tif_obj: GTiff file of the globe
    :param bbox_tup: a tuple of four float values corresponding to the bounding box
    :return: A reduced GTiff file of a specific country
    """
    global country_iso, country_dir

    output = tif_obj.split('/')[-1]
    output = country_iso + '_' + output  # tag the iso at the front
    output = country_dir + '/' + output  # make the full pathname
    file_path = Path(output)
    if file_path.exists():  # do nothing if file already there
        return
    # do gdalwarp -te bbox input output
    dataset = gdal.Warp(output, tif_obj, format='GTiff', outputBounds=bbox_tup)
    dataset = None
    return output


def tiff_to_asc(file):
    """
    This converts GTiff to ASCII file
    :param file: Tif type
    :return: ASC file
    """
    # first check if the input exists
    file_path = Path(file)
    if file_path.exists():  # proceed with transformation

        # replace .tif by .asc
        output = file.split('.')[0] + '.asc'
        # gdal_translate -of AAIGrid input.tif output.asc
        dataset = gdal.Translate(output, file, format='AAIGrid')
        dataset = None
        print('Successfully converted from GTiff to ASC')
    else:
        print('file not found: ', file)


def make_country_dir():
    """
    Creates a directory named after the iso code of a country
    :return: None
    """

    global country_iso, country_dir

    country_dir += country_iso

    if not os.path.exists(country_dir):
        os.makedirs(country_dir)


def get_country_iso(country, alpha=3):
    """
    Find and return iso code of a country
    :param country: STR- Name of a country (e.g. Thailand)
    :param alpha: INT - iso code can be 2 or 3
    :return: STR - iso code of the country (e.g. TH or THA) or None if error
    """
    try:
        country_found = pycountry.countries.search_fuzzy(country)[0]
        if alpha == 3:
            return country_found.alpha_3
        else:
            return country_found.alpha_2
    except LookupError:
        print("Can't find country: {}. Check again".format(country))
        return None


def set_country_iso(code):
    """
    A setter
    :param code: iso code (e.g. TH or THA)
    :return:
    """
    global country_iso
    country_iso = code


def get_country_bbox():
    """
    Returns the bounding box coordinates of a country
    :return:
    """
    global country_iso

    matched_bbox = [c.bbox for c in country_subunits_by_iso_code(country_iso)]
    # ensure only one country is matched
    if len(matched_bbox) != 1:
        return None
    bbox = matched_bbox[0]
    # bbox = (x_min, y_min, x_max, y_max)
    return bbox


def set_country_bbox(box):
    """
    A setter
    :param box: A tuple of 4 values
    :return: None
    """
    global country_bbox
    country_bbox = box


def interactive():
    global globe_dir, country_bbox

    # Ensure we get a valid country name
    while True:
        request_country = input("Enter country: ")
        code = get_country_iso(request_country)

        if code is None:
            continue
        else:
            break

    # Set the iso code and bounding box global vars
    set_country_iso(code)
    set_country_bbox(get_country_bbox())
    make_country_dir()

    # loop through the global geotiff to make national geotiff
    for ftif in globe_dir:
        clipped_tif = clip_by_bbox(ftif, country_bbox)
        if clipped_tif is not None:
            tiff_to_asc(clipped_tif)


def main():
    global globe_dir
    script_path = sys.argv[0]
    globe_dir = get_globe_dir(script_path)

    # no Gtiff files present
    if len(globe_dir) == 0:
        print("Global tiff files missing. Exiting...")
        return -99

    # otherwise:
    # parse the given arguments
    parser = argparse.ArgumentParser(
        description="This script extracts a national layer from global Geotiff files featuring clay, sand, organic CO "
                    "and bulk density ")
    parser.add_argument("-c", type=str, required=True, help="name of a country, e.g. Thailand")

    args = vars(parser.parse_args())

    # retrieve iso code:
    code = get_country_iso(args['c'])
    if code is None:
        print("Can't find this country:", args['c'])
        return

    # Set the iso code and bounding box global vars
    set_country_iso(code)
    set_country_bbox(get_country_bbox())
    make_country_dir()

    # loop through the global geotiff to make national geotiff
    for ftif in globe_dir:
        clipped_tif = clip_by_bbox(ftif, country_bbox)
        if clipped_tif is not None:
            tiff_to_asc(clipped_tif)
    print("Successfully extracted in the '{}' directory".format(code))


if __name__ == '__main__':
    main()
