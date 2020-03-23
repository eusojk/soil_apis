from soilapis.calculator import SoilConnector
path_name = '/home/eusoj/Downloads/gis-scripts/proj-lstfd20/layers/soilproperties/'

soil_conn = SoilConnector(path_name)

soil_taw = soil_conn.get_total_available_water(103.84, 15.76, 500, 3)
print(soil_taw)
soil_dssat = soil_conn.get_soil_property(103.84, 15.76, 500, 3, "dssat")
print(soil_dssat)