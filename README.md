soilapis
========


Requirements:
---
This module requires Gfortran and should be run on a UNIX based OS.

This module also depends on GTiff files. You can find some sample files for Thailand [here](https://www.dropbox.com/s/74hpv9d56a8s461/layers.zip?dl=0).

1. Clone this project:
```
git clone https://github.com/eusojk/soil_apis/
```
2. Run the executable to compile the required fortran scripts:
```
cd soil_apis/
chmod +x compilef90.sh 
./compilef90.sh 
```



Dependencies:
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

Usage - As a Python Module:
---

**Make sure your virtual python environment is installed and activated before proceeding**

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


Usage - As a CLI:
---

**Make sure your virtual python environment is installed and activated before proceeding**

1. Go to the location of the script

```
cd /path/to/soil_apis/soilapis
```

2. Main usage:
```
summary_soil_property.py [-h] --lon LON --lat LAT --win WIN --depth DEPTH  [--format FORMAT]
```

3. To get help:

```
summary_soil_property.py -h
```

4. For example, to get TAW file needed to to run the soil water balance:
```
python path/to/summary_soil_property.py --lon=103.84 --lat=15.76 --win=3 --depth=350
```

5. For example, To retrieve the .SOL file needed to to run DSSA:
```
python summary_soil_property.py --lon=103.84 --lat=15.76 --win=3 --depth=500 --format=dssat
```


Some References:
---
**Info on Total Available Water file:**

>
> The _SoilTAW[Depth]mm.csv_ output file contains three entries needed for Soil Water Balance:
> * _codeID_: this is a unique ID for the TAW value. It's an integer
> * _Soil type_: This is used by the water balance model to link a computational unit with the data. Possible values are: SiltLoam, SAND, SiltClayL, Loam, ClayLoam, SandyLoam, etc...
> * _TAW_: this is a float value corresponding to the TAW calculated by the script. This value is in mm
> 

**Bounding Box Coordinates: **

You can also find the bounding box coordinates for any other country [here](https://boundingbox.klokantech.com/).

Here are some examples:

> - _Cambodia_: 102.33382817, 9.4752639, 107.6276788, 14.69042236
> - _Laos_:     100.08432468, 13.90967515, 107.63499888, 22.50867163
> - _Myanmar_:  92.17194228, 9.43994314, 101.17007954, 28.54783496
> - _Thailand_: 97.34380713, 5.61285098, 105.63681192, 20.46483364
> - _Vietnam_:  102.14440999, 7.89114807, 117.86905262, 23.39339492


TODO
---
- Output .SOL file as json
