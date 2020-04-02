from soilapis.calculator import SoilConnector


def main():
    path_name = '/home/eusojk/Downloads/layers/soilproperties/'

    soil_conn = SoilConnector(path_name)

    # soil_taw = soil_conn.get_total_available_water(103.84, 15.76, 500, 3)
    # print(soil_taw)
    soil_dssat = soil_conn.get_soil_property(103.84, 15.76, 500, 3, "dssat")
    print(soil_dssat)

    # all_tif = soil_conn.get_all_tif_files()
    # for fi in all_tif:
    #     fi = glob.glob(fi)
    #     print(len(fi), type(fi))
    # print(len(all_tif), type(all_tif))


if __name__ == '__main__':
    main()
