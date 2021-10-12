# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Selection Options. Make sure that the dict name here matches the XML Node Name"""

# -- HVAC
__Mech_System = {
    "Type": {
        "attr_name": "choice",
        "enum": {
            1: "User defined (ideal system)",
        },
    },
}

__Mech_Device = {
    "SystemType": {
        "attr_name": "choice",
        "enum": {
            1: "Mechanical ventilation",
            2: "Electric resistance space heat / DHW",
            3: "Boiler",
            4: "District heating",
            5: "Heat pump",
            6: "Solar collector",
            8: "Water storage",
            10: "Photovoltaic / renewable energy",
            13: "Drain water heat recovery",
        },
    },
    "TypeDevice": {
        "attr_name": "choice",
        "enum": {
            1: "Mechanical ventilation",
            2: "Electric resistance space heat / DHW",
            3: "Boiler",
            4: "District heating",
            5: "Heat pump",
            6: "Solar collector",
            8: "Water storage",
            10: "Photovoltaic / renewable energy",
            13: "Drain water heat recovery",
        },
    },
}


# --- Geometry
__Assembly = {
    "Order_Layers": {
        "attr_name": "choice",
        "enum": {2: "from outside to inside"},
    },
    "Grid_Kind": {
        "attr_name": "choice",
        "enum": {2: "Medium"},
    },
}

__Component = {
    "OuterAttachment": {
        "attr_name": "choice",
        "enum": {
            -1: "Outer air",
            -2: "Ground",
            -3: "Space with the same inner conditions",
        },
    },
    "Type": {
        "attr_name": "choice",
        "enum": {
            1: "Opaque",
            2: "Transparent",
            3: "Opening",
        },
    },
}

__Zone = {
    "GrossVolume_Selection": {
        "attr_name": "choice",
        "enum": {
            6: "User defined",
            7: "From visualized volume and components",
        },
    },
    "NetVolume_Selection": {
        "attr_name": "choice",
        "enum": {
            4: "Estimated from gross volume",
            5: "From gross volume and components",
            6: "User defined",
            7: "From visualized volume and components",
        },
    },
    "FloorArea_Selection": {
        "attr_name": "choice",
        "enum": {
            2: "From visualized geometry",
            4: "Estimated from gross volume",
            6: "User defined",
        },
    },
    "ClearanceHeight_Selection": {
        "attr_name": "choice",
        "enum": {
            2: "Standard value",
        },
    },
    "SpecificHeatCapacity_Selection": {
        "attr_name": "choice",
        "enum": {
            1: "Lightweight",
            2: "Mixed",
            3: "Massive",
            4: "User defined",
        },
    },
}

__WP_Room = {
    "Type": {
        "attr_name": "choice",
        "enum": {1: "Kitchen", 2: "Bathroom", 3: "Shower", 4: "WC", 99: "User defined"},
    },
}


# -- PHIUS Certification settings
__PHIUS = {
    "PH_CertificateCriteria": {
        "attr_name": "choice",
        "enum": {3: "PHIUS+ 2018"},
    },
    "PH_SelectionTargetData": {
        "attr_name": "choice",
        "enum": {2: "User defined"},
    },
    "BuildingStatus": {
        "attr_name": "choice",
        "enum": {1: "In planning", 2: "Under construction", 3: "Completed"},
    },
    "BuildingType": {
        "attr_name": "choice",
        "enum": {
            1: "New construction",
            2: "Retrofit",
            3: "Mixed - new construction/retrofit",
        },
    },
    "OccupancySettingMethod": {
        "attr_name": "choice",
        "enum": {2: "Design"},
    },
}

__Occupancy = {
    "BuildingCategory": {
        "attr_name": "choice",
        "enum": {1: "Residential", 2: "Non-residential"},
    },
    "OccupancyTypeResidential": {
        "attr_name": "choice",
        "enum": {1: "Residential"},
    },
    "OccupancyTypeNonResidential": {
        "attr_name": "choice",
        "enum": {
            4: "Office/Administrative building",
            5: "School",
            6: "Other",
            7: "Undefined/unfinished",
        },
    },
}

# -- Foundations
__Foundation = {
    "FloorSlabType": {
        "attr_name": "choice",
        "enum": {
            1: "Heated basement, or underground floor slab",
            2: "Unheated basement",
            3: "Slab on grade",
            4: "Suspended floor",
            5: "None",
        },
    },
    "SettingFloorSlabType": {
        "attr_name": "choice",
        "enum": {
            2: "Detect automatically",
            6: "User defined",
        },
    },
}

# -- Appliances
__Appliances = {
    "Type": {
        "attr_name": "choice",
        "enum": {
            1: "Kitchen dishwasher",
            2: "Laundry - washer",
            3: "Laundry - dryer",
            4: "Kitchen refrigerator",
            5: "Kitchen freezer",
            6: "Kitchen fridge/freeze combo",
            7: "Kitchen cooking",
            11: "User defined",
            13: "PHIUS+ MELS",
            14: "PHIUS+ Interior lighting",
            15: "PHIUS+ Exterior lighting",
            16: "PHIUS+ Garage lighting",
            17: "User defined - lighting",
            18: "User defined - Misc electric loads",
        },
    },
    "ReferenceQuantity": {
        "attr_name": "choice",
        "enum": {
            1: "PH case occupants",
            2: "Zone occupants",
            3: "Bedroooms",
            4: "PH case Units",
            5: "User defined",
            6: "PH case floor area",
            7: "Zone floor area",
            8: "None",
        },
    },
    "ReferenceEnergyDemandNorm": {
        "attr_name": "choice",
        "enum": {
            1: "Day",
            2: "Year",
            99: "Use",
        },
    },
    "DishwasherCapacityPreselection": {
        "attr_name": "choice",
        "enum": {
            1: "Standard",
            2: "Compact",
            3: "User defined",
        },
    },
    "Connection": {
        "attr_name": "choice",
        "enum": {
            1: "DHW connection",
            2: "Cold water connection",
        },
    },
    "Dryer_Choice": {
        "attr_name": "choice",
        "enum": {
            1: "Clothesline",
            2: "Drying closet (cold)",
            3: "Drying closet (cold) at exhaust",
            4: "Condensation dryer",
            5: "Electric exhaust air dryer",
            6: "Gas exhaust air dryer",
        },
    },
    "FieldUtilizationFactorPreselection": {
        "attr_name": "choice",
        "enum": {
            1: "Timer controls",
            2: "Moisture sensing",
        },
    },
    "CookingWith": {
        "attr_name": "choice",
        "enum": {
            1: "Cooking with electricity",
            2: "Cooking with gas",
        },
    },
}
