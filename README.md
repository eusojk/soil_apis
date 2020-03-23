soilapis
========

Installation:
---
-1. create new venv
```
conda create -n testsoilapis python=3.7
conda activate testsoilapis
```
-2. Install all the dependencies:
```
 pip install -r https://raw.githubusercontent.com/eusojk/soil_apis/master/requirements.txt
```


Usage:
---
```
from soilapis.calculator import SoilConnector
```
- extract the total available water (TAW) value from soil layers. E.g:
```
soil_conn = SoilConnector(path/to/soilproperties)
soil_taw = soil_conn.get_total_available_water(103.84, 15.76, 500, 3)
print(soil_taw)
```
- create appropriate dynamic or static soil database (.SOL) as an input for DSSAT 
```
soil_conn = SoilConnector(path/to/soilproperties)
soil_dssat = soil_conn.get_soil_property(103.84, 15.76, 500, 3, "dssat")
print(soil_dssat)
```