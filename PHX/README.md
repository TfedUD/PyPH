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
        |         └── Rooms
                      ├── Room_1
        │             :    ├── Spaces (WUFI='RoomVentilation')
        │                  │   ├── Space_1
        │                  :   :   ├── Volume_1
        │                          │   └── Floor
        │                          │       ├── FloorSegment_1 
        │                          │       ├── FloorSegment_2
        │                          │       :
        │                          └── Volume_2
        │                             └── Floor
        │                                  ├── FloorSegment_1
        │                                  ├── FloorSegment_2
        │                                  :
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
For all PHX-Building-Segments, PHX-Zones and PHX-Spaces, the following structure is created:
![image](https://user-images.githubusercontent.com/69652712/135173514-5ba33e05-911f-4b06-853d-e4521e73de1b.png)

Each [BuildingSegment](https://github.com/PH-Tools/PyPH/blob/bb00e8b09c85f00161245d603ebefd06bcbaa263/PHX/bldg_segment.py#L445) can have one or more [Zones](https://github.com/PH-Tools/PyPH/blob/bb00e8b09c85f00161245d603ebefd06bcbaa263/PHX/bldg_segment.py#L320) within it. The BuildingSegment represents the largest subdivision / section of a building and can be used to represent a wing, floor, or entire building, as desired. For WUFI, this allows for the assignment of segment-wide attributes such as Residential vs. Non-Residential usage, certification thresholds, or other items input at the 'Case' level.

Each Zone can have one or more [Honeybee-Rooms](https://www.ladybug.tools/honeybee-core/docs/honeybee.room.html) within it. These Zone objects map to the 'Zone' level in WUFI and allow for zone-level assignments, especially mechanical equipment.

Below/inside of the Honeybee-Room, one or more [Space](https://github.com/PH-Tools/PyPH/blob/80b6b3c6236f931cae9df7efe2b41c403fa1a077/PHX/spaces.py#L397) objects can be added. These 'Space' objects represent the interior spatial division and sub-areas within a Honeyebee-Room. Each Space can have one or more [Volumes](https://github.com/PH-Tools/PyPH/blob/80b6b3c6236f931cae9df7efe2b41c403fa1a077/PHX/spaces.py#L303) enclosed within it. Each Volume has a single [Floor](https://github.com/PH-Tools/PyPH/blob/80b6b3c6236f931cae9df7efe2b41c403fa1a077/PHX/spaces.py#L178) which sets its lower boundary and space-shape. This Floor object is made up of one or more [FloorSegment](https://github.com/PH-Tools/PyPH/blob/80b6b3c6236f931cae9df7efe2b41c403fa1a077/PHX/spaces.py#L94) objects. This nesting is done in order to allow the user to specify individual floor segment attributes such as TFA/iCFA weighting factors, which often apply only to a portion of a Space (ie: only the area with ceiling heights under 7' or under 2.5m, etc...).

Most program-level attributes such as occupancy, lighting and ventilation will be inherited by all of the Space objects within a Honeybee Room. Any Honeybee Schedules or Loads assigned to the Room will carry through to all of the Spaces. The one exception is for Ventilation Loads, which are allowed to be set at the FloorSegment level, if the user wishes to enter that level of detail. If not, all ventilation flow rates will be inherited from the Honeybee Room.

Note: The term 'Space' is chosen consciously in this case to differentiate these PHX elements from the Honeybee 'Room' objects. In practice, for most smaller projects, a Space will map to what most would call a single 'Room'. However, Honeybee uses the term 'Room' to refer to any division or section of the building, which may lead to confusion. It is up to the user how they wish to break up or organize the zones of their model, and particularly for larger projects with many areas, it may not be practical or necessary to model every single individual space. The PHX Space is designed to be flexible enough to apply to both an individual bedroom, and an entire apartment unit.
