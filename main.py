from soilapis.calculator import SoilConnector


def main():
    path_name = '/home/eusojk/Downloads/layers/soilproperties/'

    soil_conn = SoilConnector(path_name)

    soil_taw = soil_conn.get_total_available_water(103.84, 15.76, 500, 3)
    print(soil_taw)
    soil_dssat = soil_conn.get_soil_property(103.84, 15.76, 500, 3, "dssat")
    print(soil_dssat)


if __name__ == '__main__':
    main()
