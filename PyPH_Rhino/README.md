# PyPH_Rhino:
**PyPH_Rhino** Classes and fuctions are used with the McNeel Rhinocerous / Grasshopper Application in order to build PHX Objects and Projects based on 3D Model geometry and attributes.

# PyPH_Rhino Compatability:
**PyPH_Rhino** Classes are compatible with Rhino v7+

# PyPH_Rhino Python Version:
All **PyPH_Rhino** Classes should be written to comply with Python 2.7 (IronPython) format only. Because these classes are used within the McNeel Rhinocerous/Grasshopper platform, ensure that all classes are backwards compatable to Python 2.7 / IronPython.

Note: It is recommended to include type hints for documentation purposes. For details on type hints in Pythoon 2.7, See:
[MYPY Typehints in Python 2](https://mypy.readthedocs.io/en/stable/cheat_sheet.html)

# PyPH_Rhino Usage:
Primary usage done with Grasshopper GH_Python Components. For example:

```python
# Import basic Rhino dependancies
>>> import scriptcontext as sc
>>> import Rhino as rh
>>> import rhinoscriptsyntax as rs
>>> import ghpythonlib.components as ghc
>>> import Grasshopper as gh 

# Import PyPH_Rhino dependancies
>>> import PyPH_Rhino
>>> import PyPH_Rhino.gh_io

# Create a new Grassshopper Interface
>>> IGH = PyPH_Rhino.gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )
>>> ...
```

Note that while developing / editing code in these modules, in order to update the dependancies within the GH_Python component without having to reload Grasshopper, use the reload() command. For example

```python
# import the basic dependancies
>>> import PyPH_RHino
>>> import PyPH_Rhino.gh_io

# reload the dependancies each time the GH_Python component is run
>>> reload(PyPH_Rhino)
>>> reload(PyPH_Rhino.gh_io)
>>> ...
```

This will cause the components to run more slowely since they have to reload all the packages everytime, but when development is complete these extra reload commands can be commented out / removed.