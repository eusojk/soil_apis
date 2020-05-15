from soilapis.calculator import SoilConnector


def main():
    path_name = '/home/eusojk/downloads/soil_apis/soilproperties/'
    ouput_path = "/home/eusojk/downloads/"
    soil_conn = SoilConnector(path_name)
    lon = 103.98
    lat = 11.725833333333334
    # soil_taw = soil_conn.get_total_available_water(103.84, 15.76, 500, 3)
    # print(soil_taw)
    soil_dssat = soil_conn.get_soil_property(lon, lat, 600, 20, "dssat")
    print(soil_dssat)

    # all_tif = soil_conn.get_all_tif_files()
    # for fi in all_tif:
    #     fi = glob.glob(fi)
    #     print(len(fi), type(fi))
    # print(len(all_tif), type(all_tif))


if __name__ == '__main__':
    main()
