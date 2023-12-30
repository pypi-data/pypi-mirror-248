# pyfanuc

pyfanuc is a free and open-source library allowing to connect to a Fanuc controller and to read user defined macro variables and axis related data, like positions, speeds and loads.

For detailed information about the inputs for "FocasController.read_axis()", visit: https://www.inventcom.net/fanuc-focas-library/position/cnc_rdaxisdata. For detailed information about the inputs for for "FocasController.read_macro()", visit: "https://www.inventcom.net/fanuc-focas-library/ncdata/cnc_rdmacror2".

## Installation
```
pip3 install pyfanuc

```
In case of an error message: if "fwlipy" is included, then download it manually:
```
pip3 install -e git+https://github.com/tonejca/pyfwlib.git@pyfanucable#egg=fwlipy

```

## Usage
```
from pyfanuc import FocasController

controller = FocasController("127.0.0.1")
with controller:
    axis_position = controller.read_axis(1, 0)
    macro_100 = controller.read_macro(100)
```
<!-- # Commands to build the project 
```
python3 -m pip install .

(pip3 install build twine
python3 -m build)
``` -->