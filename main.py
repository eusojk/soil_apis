from soilapis.calculator import SoilConnector


def main():
    path_name = '/home/eusojk/downloads/soilproperties/'
    ouput_path = "/home/eusojk/downloads/"
    soil_conn = SoilConnector(path_name)
    lon = 102.730077 #103.98
    lat = 16.687557 # 11.725833333333334
    soil_taw = soil_conn.get_total_available_water(103.84, 15.76, 500, 3)
    print(soil_taw)

    # list_depths = [ x for x in range(100, 520, 20)]
    # list_taw = []
    # for depth in list_depths:
    #     #soil_dssat = soil_conn.get_soil_property(lon, lat, depth, 3)
    #     soil_taw = soil_conn.get_total_available_water(lon, lat, depth, 3)
    #     print(soil_taw , depth)
    #     list_taw.append(soil_taw)
    # print(list_taw)
    
    # all_tif = soil_conn.get_all_tif_files()
    # for fi in all_tif:
    #     fi = glob.glob(fi)
    #     print(len(fi), type(fi))
    # print(len(all_tif), type(all_tif))


if __name__ == '__main__':
    main()
