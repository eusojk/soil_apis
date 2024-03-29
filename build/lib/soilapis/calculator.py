from pathlib import Path

import soilapis.extract_country_bbox as ecb
import soilapis.summary_soil_property as ssp


def get_all_tif_files():
    return ssp.get_soil_layers_dir()


class SoilConnector:
    def __init__(self, soil_layers_path, output_path=None, country='Thailand'):
        """
        Constructor
        :param soil_layers_path: main directory containing the soil properties (bulk density, organic carbon, clay, sand
        :param country: the name of the country of interest. This is set to Thailand by default
        """
        self.layers = soil_layers_path
        self.output_loc = output_path
        self.country_iso = ecb.get_country_iso(country)
        self.test_pass = self.run_tests()
        if self.test_pass:
            ssp.set_soil_layers_dir(self.layers, self.output_loc, self.country_iso)

    def get_total_available_water(self, lon, lat, depth, win):
        """
        Calculates the TAW value and return a dictionary
        :param lon: lon
        :param lat: lat
        :param depth: depth of layer
        :param win: window size of grid
        :return: a dictionary containing codeID, soil type and TAW value
        """
        if self.test_pass:
            format_arg = 'swb'
            soil_taw = ssp.setup(lon, lat, win, format_arg, depth, json_out=True)
            return soil_taw

    def get_soil_property(self, lon, lat, depth, win, format_arg):
        """
        Similar to get_TAW to the exception of returning a .SOL file needed for DSSAT
        :param lon: lon
        :param lat: lat
        :param depth: depth of layer
        :param win: window size of grid
        :param format_arg: dssat (a .SOL file) or dssat_json (a json type output) or error codes: -99 or -89 (sea values)
        :return:
        """
        if self.test_pass:
            if format_arg == "dssat_json":
                format_arg = 'dssat'
                soil_dssat_json = ssp.setup(lon, lat, win, format_arg, depth, json_out=True)
                return soil_dssat_json

            elif format_arg == "dssat":
                soil_dssat_sol = ssp.setup(lon, lat, win, format_arg, depth)
                return soil_dssat_sol

            else:
                print('Not recognized:', format_arg)
                return

    def run_tests(self):
        """
        Check that country and layers directory are both valid
        :return: bool
        """
        if self.country_iso is None:
            return
        if not Path(self.layers).exists():
            print("Given directory doesn't exit:", self.layers)
            return
        if self.output_loc is not None:
            if not Path(self.output_loc).exists():
                print("Given output directory doesn't exit:", self.output_loc)
                return

        self.test_pass = True

        return self.test_pass

    def print(self):
        pass
