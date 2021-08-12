# PHX Model:
The PHX (Passive House Exchange) model is a generic Passive-House data model which can be used by Passive House software for input / output and translation accross different patforms (PHPP, WUFI, C3RRO, Ladybug, etc.).

# PHX Class Behavior:
All PHX classes are generic to any specific program and primarily used to store and organize object data / attributes. Class behavior should be limited to data storage, cleaning, manipluation and validation. All program specific behavior should be moved to separate modules and packages.

All PHX Classes do include native serialization through the Obj.to_dict() and Obj.from_dict() methods. These methods work with Python dictionaries only and further export (to JSON, to XML) is done in separate modules.

# PHX Python Version:
All PHX Classes should be written to comply with Python 2.7 (IronPython) format only. Because these classes are used within the McNeel Rhinocerous/Grasshopper platform, ensure that all classes are backwards compatable to Python 2.7 / IronPython.

Note: It is recommended to include type hints for documentation purposes. For details on type hints in Pythoon 2.7, See:
[MYPY Typehints in Python 2](https://mypy.readthedocs.io/en/stable/cheat_sheet.html)

Note: Grasshopper IronPython does NOT inlcude the 'typing' module for some reason - ensure that no PHX modules 'import typing' or it will throw an error when Grasshopper attempts to import.

# PHX Class Usage:
Most PHX classes are not designed to be 'run' on their own. These classes are data classes which are used by other interfaces (Rhino, WUFI, PHPP, etc.)

# PHX Model Structure:
Ths primary structure / nesting of a PHX 'Project' would look like the following:
(note: Object attribute fields ommitted for clarity)
```bash
Project
├── Assemblies
│   └── Layers
│         ├── Material_1 (ref)
│         ├── Material_2 (ref)
│         :
├── Materials
├── Window Types
└── BuildingSegments (WUFI='Variant/Case')
   ├── Segment_01  
   :    ├── Climate / Location
        ├── Components
        │     ├── Component_1
        │     │   ├── Polygon_1 (ref) 
        │     │   ├── Polygon_2 (ref)
        │     │   :
        │     ├── Component_2
        │     :   ├── Polygon_3 (ref)
        │         ├── Polygon_4 (ref)
        │         :
        │
        ├── Zones (WUFI='Zone')
        │     └── Zone_1
        │         ├── Spaces (WUFI='Room')
        │         │   ├── Space_1
        │         :   :   ├── Volume_1
        │                 │   └── Floor
        │                 │       ├── FloorSegment_1 
        │                 │       ├── FloorSegment_2
        │                 │       :
        │                 └── Volume_2
        │                    └── Floor
        │                         ├── FloorSegment_1
        │                         ├── FloorSegment_2
        │                         :
        ├── Geometry
        │    ├── Polygons
        │    │   ├── Polygon_1
        │    │   ├── Polygon_2
        │    │   ├── Polygon_3
        │    │   ├── Polygon_4
        │    │   :
        │    └── Vetices
        │        ├── Vertex_1
        │        ├── Vertex_1
        │        :
        ├── HVAC
        │   └── ...
        :
```
