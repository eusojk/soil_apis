import argparse
import glob
import os
import sys
from pathlib import Path

# from fortran_apis import which_api
from soilapis.fortran_apis import which_api
import gdal
import osr
import pandas as pd

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
gdal.UseExceptions()  # Enable errors


class CountrySoilProperty(object):

    def __init__(self, fname):
        """

        :param fname: a GTif file
        """
        try:
            self.raster = gdal.Open(fname)
            spatial_ref = osr.SpatialReference(self.raster.GetProjection())

            # retrieve get the WGS84 spatial reference
            wgs_ref = osr.SpatialReference()
            wgs_ref.ImportFromEPSG(4326)

            # Do a coordinate transform
            self.coord_transf = osr.CoordinateTransformation(wgs_ref, spatial_ref)

            # Apply geo-transformation and its inverse
            self.raster_gt = self.raster.GetGeoTransform()
            self.raster_inv_gt = gdal.InvGeoTransform(self.raster_gt)

            # Handle error from Inverse function
            if gdal.VersionInfo()[0] == '1':
                if self.raster_inv_gt[0] == 1:
                    self.raster_inv_gt = self.raster_inv_gt[1]
                else:
                    raise RuntimeError('Inverse geotransform failed')
            elif self.raster_inv_gt is None:
                raise RuntimeError('Inverse geotransform failed')

        except RuntimeError:  # <- Check first what exception is being thrown
            pass


    def get_px_coord(self, lon, lat):
        """
        Convert lon-lat into x-y coordinates of pixel
        :param lon: longitude
        :param lat: latitude
        :return: tuple of pixel coordinates
        """
        offsets_coord = gdal.ApplyGeoTransform(self.raster_inv_gt, lon, lat)
        px_x, px_y = map(int, offsets_coord)

        return px_x, px_y

    def get_band_array(self):
        """

        :return: 2D array of the rater file
        """
        return self.raster.GetRasterBand(1).ReadAsArray()

    def get_band_value(self, lon, lat):
        """
        Extract the pixel value at a given position
        :param lon: lon
        :param lat: lat
        :return: int - pixel value
        """
        px_x, px_y = self.get_px_coord(lon, lat)

        return self.get_band_array()[px_y, px_x]

    def average_by_window(self, lon, lat, window_size=3):
        """
        This function slice a big array based on a given window size
        :param lon: longitude
        :param lat: latitude
        :param window_size: int - height and width of window. e.g. 3 means 3 by 3. Must be odd
        :return: float value, the average or mean of the array or -99 if invalid
        """
        if self.get_band_value(lon, lat) == 255:  # disregard any value from the sea
            return - 99

        array = self.slice_by_window(lon, lat, window_size)
        if array is None:
            return -99
        return round(array.mean(), 2)

    def slice_by_window(self, lon, lat, window_size):
        """
        This function slice a big array based on a given window size
        :param lon: longitude
        :param lat: latitude
        :param window_size: int - height and width of window. e.g. 3 means 3 by 3. Must be odd
        :return: a 2D array or None
        """
        px_x, px_y = self.get_px_coord(lon, lat)

        if window_size % 2 == 0:  # degrade to lower odd number. eg. 4 => 3
            window_size -= 1
            if window_size < 3:
                window_size = 3

        step = (window_size - 1) // 2
        row_start = px_x - step
        row_stop = px_x + step + 1
        col_start = px_y - step
        col_stop = px_y + step + 1
        data = self.get_band_array()
        res = data[row_start:row_stop, col_start:col_stop]
        if res.shape[0] * res.shape[1] != window_size * window_size:
            return
        return res


def set_soil_layers_dir(soil_layers_path, country_iso):
    global bds_dir, cla_dir, org_dir, san_dir, dir_types

    dir_types = []
    layers_types = ['bulkdensity', 'clay', 'organicsoil', 'sandfraction']

    for lt in layers_types:
        path_obj = soil_layers_path + lt + '/' + country_iso
        if Path(path_obj).exists():
            path_obj += '/*.tif'
            dir_types.append(path_obj)


def get_soil_layers_dir():
    global dir_types
    # for t in glob.glob(dir_types[0]):
    #     print(t)

    return dir_types


def ini_dir(script_path):
    """
    Initializes important paths
    :param script_path: the abs pathname of the script
    :return: None
    """
    global script_dir, outputs, parent_dir, layers_dir, country_dir, globe_dir, soilp_dir, \
        bds_dir, cla_dir, org_dir, san_dir, dir_types
    script_dir = os.path.abspath(script_path)

    script_dir = os.path.abspath(os.path.dirname(script_path))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    layers_dir = parent_dir + '/layers/'
    country_dir = layers_dir + 'country/'
    globe_dir = layers_dir + 'globe/*.tif'
    globe_dir = glob.glob(globe_dir)
    soilp_dir = layers_dir + 'soilproperties/'
    bds_dir = soilp_dir + 'bulkdensity/THA/*.tif'
    cla_dir = soilp_dir + 'clay/THA/*.tif'
    org_dir = soilp_dir + 'organicsoil/THA/*.tif'
    san_dir = soilp_dir + 'sandfraction/THA/*.tif'
    dir_types = [bds_dir, cla_dir, org_dir, san_dir]
    outputs = script_dir + '/outputs/'


def get_globe_dir(script_path):
    """
    Return the pathnames of global tiff files
    :param script_path: the abs pathname of this script
    :return: abs pathname of the globe tif files as a list
    """
    ini_dir(script_path)
    return globe_dir


def set_globe_dir(global_layers_dir):
    """
    Set the path to dir that contains the global Gtif layers
    :param global_layers_dir:
    :return:
    """
    global globe_dir

    globe_dir = global_layers_dir + '*.tif'
    globe_dir = glob.glob(globe_dir)


def average_per_layer(dir_path, lon, lat, window_size):
    """

    :param dir_path:
    :param lon:
    :param lat:
    :param window_size:
    :return:
    """
    list_avg = []
    dir_path = glob.glob(dir_path)

    for tf in dir_path:
        co = CountrySoilProperty(tf)
        avg = co.average_by_window(lon, lat, window_size)
        if avg == -99:
            return -99
        list_avg.append(avg)

    return list_avg


def average_per_type(dir_path, lon, lat, window_size):
    """

    :param dir_path:
    :param lon:
    :param lat:
    :param window_size:
    :return:
    """
    dict_avg = {}
    for path in dir_path:
        key = path.split('/')[-3]
        list_avg = average_per_layer(path, lon, lat, window_size)

        if list_avg == -99:
            return -99

        if key not in dict_avg:
            dict_avg[key] = list_avg

    return dict_avg


def dict_to_df(dict_name):
    """

    :param dict_name:
    :return:
    """
    return pd.DataFrame.from_dict(dict_name)


def df_to_asc(dfname, outname):
    """

    :param outname:
    :param dfname:
    :return:
    """
    dfname.to_csv(outname, sep='\t', encoding='utf-8', index=False)


def compute_pwp_row(col):
    """

    :param col: pandas col
    :return:
    """
    clay_val = col['clay']
    oc_val = col['organicsoil']
    sand_val = col['sandfraction']

    return compute_pwp(clay_val, oc_val, sand_val)


def compute_pwp(clay_val, oc_val, sand_val):
    """
    Calculate permanent wilting point based on Clay, Organic Matter and sand value
    :param clay_val: percentage of clay
    :param oc_val: percentage of organic carbon
    :param sand_val: percentage of sand
    :return: a float value representing PWP
    """

    # Step #1 - convert OC to OM
    om_val = 2 * oc_val
    om_val /= 1000
    clay_val /= 100
    sand_val /= 100

    # Step #2 - compute theta_1500_t
    theta_1500_t = 0.031 - (0.024 * sand_val) + (0.487 * clay_val) + (0.006 * om_val) \
                   + (0.005 * sand_val * om_val) - (0.013 * clay_val * om_val) + (0.068 * sand_val * clay_val)

    # Step #3 - finally compute theta_1500
    theta_1500 = (1.14 * theta_1500_t) - 0.02

    return round(theta_1500, 2)


def compute_fc_row(col):
    """

    :param col: pandas col
    :return:
    """
    clay_val = col['clay']
    oc_val = col['organicsoil']
    sand_val = col['sandfraction']

    return compute_field_capacity(clay_val, oc_val, sand_val)


def compute_field_capacity(clay_val, oc_val, sand_val):
    """
    Calculate Field Capacity based on Clay, Organic Matter and sand value
    :param clay_val: percentage of clay
    :param oc_val: percentage of organic carbon
    :param sand_val: percentage of sand
    :return: a float value representing FC
    """

    # Step #1 - convert OC to OM
    om_val = 2 * oc_val
    om_val /= 1000
    clay_val /= 100
    sand_val /= 100

    # Step #2 - compute theta_33_t
    theta_33_t = 0.299 - (0.251 * sand_val) + (0.195 * clay_val) + (0.011 * om_val) \
                 + (0.006 * sand_val * om_val) - (0.027 * clay_val * om_val) + (0.452 * sand_val * clay_val)

    # Step #3 - compute actual F.C: theta_33
    theta_33 = theta_33_t + ((1.283 * theta_33_t * theta_33_t) - (0.374 * theta_33_t) - 0.015)

    return round(theta_33, 2)


def compute_taw(fc, pwp, depth, fraction):
    """
    Compute total available water
    :param fc: Field capacity
    :param pwp: permanent wilting point
    :param depth: depth of soil in mm
    :param fraction: float value
    :return: a float value for TAW
    """

    return depth * fraction * (fc - pwp)


def compute_taw_row(row):
    """

    :param row: a pandas data frame object
    :return: a float value for TAW
    """
    fc = row['FC']
    pwp = row['PWP']
    depth = row['depths']
    fraction = row['fraction']
    return compute_taw(fc, pwp, depth, fraction)


def setup(lon, lat, window, format_arg, depth=0, json_out=False):
    """

    :param lon: longitude
    :param lat: latitude
    :param window: window size. e.g. 3 means 3 by 3
    :param depth: depth of soil in mm
    :param format_arg: str - indicates type of output to produce. if 'swb', output is TAW file; if 'dssat', output is .SOL file
    :return: a text file or -99
    :param json_out: if True, return a dict, otherwise a text file
    """
    global outputs, dir_types, script_dir
    out_dssat = script_dir
    # script_dir += '/soilapis/'
    outputs = script_dir + '/outputs'
    if not os.path.exists(outputs):
        os.makedirs(outputs)
    # test =  Path(script_dir).exists()
    # print('script_dir', test)
    # os.chdir(outputs)
    # you could change the lat long in the following:
    dict_summary = average_per_type(dir_types, lon, lat, window)
    if dict_summary == -99:
        return -99

    # outname = outputs
    # outname = 'taw-' + str(lon) + '-' + str(lat) + '-' + str(depth) + 'mm.csv'
    outname = 'SoilTAW' + str(depth) + 'mm.csv'

    depth_values = [10, 90, 200, 300, 400, 1000]
    frac_values = []
    actual_frac = 1

    # Estimating closest depth value if depth given is part of depth values available
    if depth not in depth_values:
        depth_possible = [abs(x - depth) for x in depth_values]
        min_diff = min(depth_possible)
        index_closest = depth_possible.index(min_diff)
        depth_closest = depth_values[index_closest]
        depth_diff = abs(depth - depth_closest)
        actual_frac = depth_diff / depth_values[index_closest]

    else:  # depth given is available
        # depth = depth_values[0]
        # layer_oi = str(depth) + 'mm'
        index_closest = depth_values.index(depth)

    # compute the fractions needed for computing TAW
    for i in range(len(depth_values)):
        if i < index_closest:
            frac = 1
        elif i == index_closest:
            frac = round(actual_frac, 2)
        else:
            frac = 0
        frac_values.append(frac)

    # make a dataframe
    df_summary = dict_to_df(dict_summary)

    # divide current bulk density values by 100
    df_summary['bulkdensity'] = round(df_summary['bulkdensity'] / 100, 2)
    df_summary = round(df_summary, 2)
    df_summary['Latitude'] = lat
    df_summary['Longitude'] = lon
    df_summary['Depth'] = depth

    # export dataframe as csv to produce .SOL
    if format_arg == 'dssat':
        ascfile = out_dssat + '/sample_asc.csv'
        df_to_asc(df_summary.iloc[:, 0:8], ascfile)
        out_path_asc = os.path.abspath(ascfile)
        out_path = which_api(out_path_asc, script_dir, 1)

        # TO-DO: convert TH.SOL into JSON. Ask Jab's advice
        if json_out:
            pass

    # Otherwise, let's make a SoilTAW file
    else:
        df_summary.insert(0, 'depths', depth_values)
        df_summary['FC'] = df_summary.apply(compute_fc_row, axis=1)
        df_summary['PWP'] = df_summary.apply(compute_pwp_row, axis=1)
        df_summary['fraction'] = frac_values
        df_summary['TAW'] = df_summary.apply(lambda x: compute_taw_row(x), axis=1)

        # taw_val = df_summary.loc[layer_oi, 'TAW']
        taw_val = df_summary['TAW'].sum()
        taw_val = round(taw_val, 2)

        # Extract sand and clay value needed to estimate soil type
        fracs = [df_summary['sandfraction'].iloc[0], df_summary['clay'].iloc[0]]

        # call the fortran_api
        out_path_asc = os.path.abspath(outname)
        soil_type = which_api(out_path_asc, script_dir, 0, fracs)

        taw_dict = {"Code": 1, "Soil": soil_type, 'Total_Available_Water(mm)': taw_val}

        if json_out is True:
            return taw_dict

        taw_dict = {"Code": [1], "Soil": [soil_type], 'Total_Available_Water(mm)': [taw_val]}
        taw_data = pd.DataFrame.from_dict(taw_dict)

        # export df as a txt/csv file
        df_to_asc(taw_data, outname)
        out_path = os.path.abspath(outname)

    return out_path


def interactive_run():
    """
    This function runs the script in interactive mode
    :return: None
    """
    # Check that all necessary files are present
    script_path = sys.argv[0]
    ini_dir(script_path)

    # setup(102.765, 13.369, 3, 1000)

    print(
        "\nThis script is currently only supporting Thailand. Using geo coordinates not associated with this country "
        "will give misleading results!\n")

    # Check if the soil properties directory is present before running
    layers_dir_path = Path(layers_dir)
    layers_dir_present = layers_dir_path.exists()
    while layers_dir_present:
        prompt = input("Enter 'R' to (re)start or 'Q' to quit: ")
        print()
        if prompt.lower() == 'r':
            while True:
                try:
                    lon = float(input("Enter longitude: "))
                    lat = float(input("Enter latitude: "))
                    window = int(input("Enter window size (e.g. enter '3' for 3x3): "))
                    depth = int(input("Enter soil depth (mm): "))

                except ValueError:
                    print('Invalid key. Please enter a numerical value')
                    continue

                outname = setup(lon, lat, window, depth)
                if outname == -99:
                    print("\nInvalid location. This lon({}) and lat({}) is definitely in the sea.".format(lon, lat))
                else:
                    print('Check directory for the following file: ', outname)

                setup_prompt = input('\nWould you like to make a new simulation? (y or n): ')

                if setup_prompt.lower() == 'y':
                    continue
                elif setup_prompt.lower() == 'n':
                    break
                else:
                    print('Got invalid response. Restarting...')

        elif prompt.lower() == 'q':
            print('Exiting...')
            break
        else:
            print("Sorry, invalid key... \n")
            continue
    else:
        print(
            "\n The 'layers' directory is missing. Please download the zip file and place it in your project directory.")


def main():
    # Check that all necessary files are present
    script_path = sys.argv[0]
    ini_dir(script_path)

    # Check if layers directory exists
    layers_dir_path = Path(layers_dir)
    layers_dir_present = layers_dir_path.exists()

    if not layers_dir_present:
        print(
            "\n The 'layers' directory is missing. Please download the zip file and place it in your project directory.")
        return

    # parse the given arguments
    parser = argparse.ArgumentParser(
        description="This script interpolates TAW value for a specific location in Thailand"
    )
    parser.add_argument("--lon", type=float, required=True, help="longitude value, e.g. 103.98")
    parser.add_argument("--lat", type=float, required=True, help="latitude value, e.g. 15.88")
    parser.add_argument("--win", type=int, required=True, help="window size, e.g. enter '3' for a window size "
                                                               "of 3x3")
    parser.add_argument("--depth", type=int, required=True, help="depth value in mm, e.g. 350")
    parser.add_argument("--format", default='swb', type=str, required=False,
                        help="options are: 'swb' to produce SoilTAW file or 'dssat' to produce .SOL ")

    args = vars(parser.parse_args())
    # check the value of the format given: should be None ('swb') or 'dssat'
    if (args['format'] == 'swb') or (args['format'] == 'dssat'):
        outname = setup(args["lon"], args["lat"], args["win"], args['format'], args["depth"])
        if outname == -99:
            print("\nInvalid location. This lon({}) and lat({}) is definitely in the sea.".format(args["lon"],
                                                                                                  args["lat"]))
        else:
            print('Check directory for the following file: ', outname)
    else:
        print("Invalid format argument: '{}'. Please choose either 'swb' or 'dssat'".format(args['format']))


if __name__ == '__main__':
    main()
    # interactive_run()
