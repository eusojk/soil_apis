import os
import glob
import argparse
import sys
import pandas as pd
import soilapis.extract_country_bbox as ecb
from pathlib import Path
from soilapis.calculator import SoilConnector
from shutil import copyfile, copyfileobj

dirname = ''

def make_static_soil_db(soil_dir, country='Thailand'):
    """
    Main function to create the static SOL
    :param soil_dir: main directory containing the soil properties (bulk density, organic carbon, clay, sand
    :param country: the name of the country of interest. This is set to Thailand by default
    :return: pathname to the final .SOL
    """

    # what is the iso code of this country?
    country_iso = ecb.get_country_iso(country)

    # check if country is valid
    if country_iso is None:
        return

    # check if this country is suitable for the script:
    if is_loc_file_present(country_iso) is None:
        print("{} is not currently supported :(".format(country))
        return
    else:
        print("UOUOIUOJUOI!")
        return

    lon_lat_fn = is_loc_file_present(country_iso)[0]
    lon_lat_df = pd.read_csv(lon_lat_fn)
    lon_df = lon_lat_df['lon']
    lat_df = lon_lat_df['lat']

    # set output directory
    output_dir = is_loc_file_present(country_iso)[1]
    # print("output_dir", output_dir)
    os.chdir(output_dir)

    # create an instance of soil connector
    soil_conn = SoilConnector(soil_dir)
    depth_arg = 600
    win_size = 20
    format_arg = "dssat"
    error_codes = [-89, -99]
    # how many rows do we need to loop through
    num_rows = lon_lat_df.shape[0]

    # naming convention: TH_000000*
    name_conv = country_iso + '_' + (len(str(num_rows)) + 1) * '0'
    len_name_conv = len(name_conv)

    # Manufacture each dynamic .SOL for each point
    for row_i in range(num_rows):
        # get them lon, lat
        lon = lon_df.iloc[row_i]
        lat = lat_df.iloc[row_i]

        # create the dynamic .SOL for this point
        soil_dssat = soil_conn.get_soil_property(lon, lat, depth_arg, win_size, format_arg)

        # Watch out for sea values:
        if soil_dssat in error_codes:
            continue

        # fix the code in TH.SOL:
        digt = str(row_i + 1)
        len_i = len(digt)
        cut_at = len_name_conv - len_i
        cut_val = name_conv[:cut_at]
        new_code = cut_val + digt
        fix_code_num_in_sol(new_code, soil_dssat)

        new_name_i = str(output_dir) + '/' + new_code + '.SOLD'

        copyfile(soil_dssat, new_name_i)
        print('Writing: ', new_name_i)
        # if row_i == 2:
        #     break

    # Main static file
    dot_sol_output = str(output_dir) + '/' + country_iso + '.SOL'
    dot_sol_path = merge_all_dot_sol(output_dir, dot_sol_output, num_rows)

    # remove dynamic .SOL
    remove_dynamic_dot_sol(output_dir)

    return dot_sol_path


def fix_code_num_in_sol(new_code, sol_file):
    """
    The dynamic .SOL has a hardcoded codename (e.g. TH_00001). We need to change that
    :param new_code: new code to substitute
    :param sol_file: the file to correct
    :return:
    """
    from_file = open(sol_file)
    hline = from_file.readline()

    hline_new = "*" + new_code + hline[12:]

    to_file = open(sol_file, mode="w")
    to_file.write(hline_new)
    copyfileobj(from_file, to_file)
    # print(hline)
    # print(hline_new)


def merge_all_dot_sol(outputs_dir, dot_sol_output, num_rows):
    """
    Merge all .SOL into one
    :param outputs_dir: directory containing the dynamic .SOL
    :param dot_sol_output: file to write the content to. This is the static .SOL
    :param num_rows: number of points. This is to make sure that all dynamic SOL are written
    :return: pathname to the final .SOL file
    """
    # get all the dynamic .SOL
    match = str(outputs_dir) + '/*.SOLD'

    all_dot_sols = glob.glob(match)
    all_dot_sols.sort()

    # for i in all_dot_sols:
    #     print(i)

    # if len(all_dot_sols) != num_cells: # something wrong
    #     print("Stopping: The static database seems not complete")
    #     return

    with open(dot_sol_output, "wb") as outfile:
        for f in all_dot_sols:
            with open(f, "rb") as infile:
                outfile.write(infile.read())
                outfile.write('\n'.encode())
    dot_sol_output = str(outputs_dir) + '/' + dot_sol_output
    return Path(dot_sol_output)


def is_loc_file_present(country_iso):
    """
    checks if the file containing the lat and lon values of a country is present
    :param country_iso: a 3 string value: representing the iso code of a country. e.g; tha for Thailand
    :return: pathname a tuple if file exists, None otherwise
    """
    global dirname

    country_iso = country_iso.lower()
    script_dir = dirname #os.getcwd()
    # script_dir = os.path.abspath(os.path.dirname(script_dir))

    output_dir = script_dir + '/outputs/'
    output_dir = Path(output_dir)

    locs_dir = script_dir + '/locs/'
    loc_file = locs_dir + country_iso + '_lon_lat_centers.csv'

    # print('script_dir:',script_dir)
    # print('loc_file:',loc_file)
    # print('dirname:',dirname)

    # loc_file = Path(loc_file)
    if os.path.exists(loc_file):
        return loc_file, output_dir
    else:
        return


def remove_dynamic_dot_sol(dot_sol_dir):
    """
    Remove dynamic .SOL's
    :param dot_sol_dir: directory containing the dynamic .SOL
    :return: None
    """
    match = str(dot_sol_dir) + '/*.SOLD'

    all_dot_sols = glob.glob(match)
    for fl in all_dot_sols:
        # print(os.path.isfile(fl), fl)
        if os.path.isfile(fl):
            os.remove(fl)
        else:
            print("Error - deleting:", fl)


def is_soil_layers_present(script_path):
    global dirname

    script_dir = os.path.abspath(os.path.dirname(script_path))
    dirname = script_dir
    layers_dir = script_dir + '/soilproperties/'

    if not Path(layers_dir).exists():
        return
    # print("layers_dir", Path(layers_dir).exists(), layers_dir)
    return layers_dir


def main():
    path_name = '/home/eusojk/Downloads/layers/soilproperties/'
    # print(make_static_soil_db(path_name))

    arg1 = "/home/eusojk/PycharmProjects/soil_apis/outputs"
    # arg2 = 'TTT.SOL'
    # merge_all_dot_sol(arg1, arg2)

    # remove_dynamic_dot_sol(arg1)
    script_path = sys.argv[0]
    soil_dir = is_soil_layers_present(script_path)

    if soil_dir is None:
        print(
            "\n The 'soilproperties' directory is missing. Please download the zip file and place it in your project directory.")
        return

    parser = argparse.ArgumentParser(
        description="This script creates a static soil database .SOL"
    )
    parser.add_argument("--country", type=str, required=True, help="country, e.g. Thailand")
    country_arg = vars(parser.parse_args())['country']
    # print(country_arg, soil_dir)

    make_static_soil_db(soil_dir, country_arg)


if __name__ == '__main__':
    main()
