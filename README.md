soilapis
========

Installation:
---
-1. create new venv and Install all the dependencies:
```
conda create -n testsoilapis python=3.7
conda activate testsoilapis
pip install -r https://raw.githubusercontent.com/eusojk/soil_apis/master/requirements.txt
```
-2. Fix GDAL's build errors with conda-forge:
```
 conda install -c conda-forge gdal
```
-3. Finally install module:
```
 pip install https://github.com/eusojk/soil_apis/blob/master/soilapis.zip?raw=true
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