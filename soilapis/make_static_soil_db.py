import os
import sys
import soilapis.extract_country_bbox as ecb
from pathlib import Path

from soilapis.calculator import SoilConnector


def make_static_soil_db(country='Thailand'):
    country_iso = ecb.get_country_iso(country)

    # check if country is valid
    if country_iso is None:
        return

    # check if this country is suitable for the script:
    if is_loc_file_present(country_iso) is None:
        print("{} is not currently supported :(".format(country))
        return

    print(country, is_loc_file_present(country_iso))


def is_loc_file_present(country_iso):
    """
    checks if the file containing the lat and lon values of a country is present
    :param country_iso: a 3 string value: representing the iso code of a country. e.g; tha for Thailand
    :return: pathname if file exists, None otherwise
    """
    country_iso = country_iso.lower()
    script_dir = os.getcwd()
    script_dir = os.path.abspath(os.path.dirname(script_dir))
    locs_dir = script_dir + '/locs/'
    loc_file = locs_dir + country_iso + '_lon_lat_centers.csv'

    loc_file = Path(loc_file)

    return loc_file if loc_file.exists() else None


def main():
    make_static_soil_db()


if __name__ == '__main__':
    main()
