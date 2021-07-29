# PyPH_HBJSON
PyPH_HBJSON classes are used to import a Honeybee JSON file (*.hbjson) and convert it into a PHX model. This model can then be edited or exported to another platform via modules such as PyPH_WUFI or PyPH_PHPP.

# PyPH_HBJSON Compatability:
PyPH_HBJSON importers are compatible with Honeybee-Schema v1.43.6

# PyPH_HBJSON Python Version:
All PyPH_HBJSON Classes should be written to comply with **Python 3.9+** format.

# PyPH_HBJSON Usage:
In order to import an existing .hbjson file:

```python
# Import the HB-JSON reader & converter functions
>>> from PyPH_HBJSON.read_HBJSON_file import read_hb_json
>>> from PyPH_HBJSON.create_PHX_Zones import create_zone_from_HB_room

# Supply the path to the existing .hbjson file, read in the file
>>> SOURCE_FILE = "my_example_dir/example_file.hbjson"
>>> hb_model = read_hb_json(SOURCE_FILE)
>>> 

# You can now work through the HB-Model elements and convert HB-Objects to PHX-Objects as desired. For example:
>>> for hb_room in hb_model.rooms:
>>>     new_PHX_zone = create_zone_from_HB_room( hb_room )
>>> ...
```
