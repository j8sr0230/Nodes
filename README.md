# FreeCAD Nodes

A visual scripting environment for [FreeCAD](https://www.freecad.org) using 
[pyqt-node-editor](https://gitlab.com/pavel.krupala/pyqt-node-editor) 
from Pavel Křupala.

![FreeCAD Nodes](https://github.com/j8sr0230/fc_nodes/blob/main/img/fcn_nested_array.png)
<!-- Add screenshots here -->

## Prerequisites
* FreeCAD >= LinkDaily 2022.430.26244 +4758 (Git)
* or FreeCAD >= v0.20 (not tested yet)

## Installation
FreeCAD Nodes uses the [pyqt-node-editor](https://gitlab.com/pavel.krupala/pyqt-node-editor) 
from Pavel Křupala as node editor framework and [Awkward Array](https://awkward-array.readthedocs.io/en/stable/) for 
handling nested, variable-sized data structures. You can install the latest versions via **pip of your FreeCAD 
environment** with the following command.
```
$ pip install git+https://gitlab.com/pavel.krupala/pyqt-node-editor.git
$ pip install awkward
```

Subsequently, download the archive `fc_nodes-main.zip` from this repo (Code > Download ZIP) 
and unpack it at your preferred location.

The last thing you have to do is to set the FreeCAD macro directory to the path of 
the unzipped `fc_nodes-main` folder and restart FreeCAD.

Now you can run the file `main.py` as a FreeCAD macro.

## Usage
### Feature overview
![Feature overview](https://github.com/j8sr0230/fc_nodes/blob/main/img/fcn_base_node_features.gif)
Tutorials coming soon!

## License

LGPLv2.1 ([LICENSE](LICENSE))