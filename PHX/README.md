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


# PHX Spaces:
For all PHX Spaces, the following structure is created:

![image](https://user-images.githubusercontent.com/69652712/133120470-a8be904f-2b22-4e7e-8011-81e47d2784e0.png)

Each [Space](https://github.com/PH-Tools/PyPH/blob/80b6b3c6236f931cae9df7efe2b41c403fa1a077/PHX/spaces.py#L397) can have one or more [Volumes](https://github.com/PH-Tools/PyPH/blob/80b6b3c6236f931cae9df7efe2b41c403fa1a077/PHX/spaces.py#L303) encolsed within it. Each Volume has a single [Floor](https://github.com/PH-Tools/PyPH/blob/80b6b3c6236f931cae9df7efe2b41c403fa1a077/PHX/spaces.py#L178) which sets its lower boundary and shape. This Floor object is made up of one or more [FloorSegment](https://github.com/PH-Tools/PyPH/blob/80b6b3c6236f931cae9df7efe2b41c403fa1a077/PHX/spaces.py#L94) objects. This nesting is done in order to allow the user to specify individual floor segment attributes such as TFA/iCFA weighting factors, which often apply only to a portion of a Space (ie: only the area with ceiling heights under 7' or under 2.5m, etc...).

Note: The term 'Space' is chosen consciously in this case to differentiate these PHX elements from the Honeybee ['Room'](https://www.ladybug.tools/honeybee-core/docs/honeybee.room.html) objects. In practice, for most smaller projects, a Space will map to what most would call a single 'Room'. However, Honeybee uses the term 'Room' to refer to any division or section of the building, which may lead to confusion. It is up to the user how they wish to break up or organize the zones of their model, and particularly for larger projects with many areas, it may not be practical or necessary to model every single individual space. The PHX Space is designed to be flexible enough to apply to both an individual bedroom, and an entire apartment unit.
