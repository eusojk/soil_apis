"""
    This script creates a sub map of a country clipped from globe data file
"""
import argparse
import os
import sys
from pathlib import Path

import gdal
import pycountry
from country_bounding_boxes import country_subunits_by_iso_code


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
    
    file_path = Path(output)
    if file_path.exists():  # do nothing if file already there
        return
    # do gdalwarp -te bbox input output
    dataset = gdal.Warp(output, tif_obj, format='GTiff', outputBounds=bbox_tup)
    dataset = None
    output = os.path.abspath(output)
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

def main():


    parser = argparse.ArgumentParser(
        description="This script extracts a national layer from global Geotiff files featuring clay, sand, organic CO "
                    "and bulk density ")
    parser.add_argument("-c", type=str, required=True, help="name of a country, e.g. Thailand")
    parser.add_argument("-g", type=str, required=True, help="path to global geotif file, e.g. /downloads/clay.tiff")

    args = vars(parser.parse_args())

    # retrieve iso code:
    code = get_country_iso(args['c'])
    name_global_tiff = args['g']

    if code is None:
        print("Can't find this country:", args['c'])
        print("Exited")
        return

    if not Path(name_global_tiff).exists():
        print("File: {} not found.".format(name_global_tiff))
        print("Exited")
        return

    # Set the iso code and bounding box global vars
    set_country_iso(code)
    set_country_bbox(get_country_bbox())

    clipped_tif = clip_by_bbox(name_global_tiff, country_bbox)

    if clipped_tif is not None:
        print('Extraction terminated. Output:', clipped_tif)

if __name__ == '__main__':
    main()
