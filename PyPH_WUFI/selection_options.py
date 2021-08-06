# -*- coding: utf-8 -*-
# -*- Python Version: 3.x -*-

"""Selection Options. Make sure that the dict name here matches the XML Node Name"""

__HVAC_System = {
    "Type": {
        "attr_name": "choice",
        "enum": {
            1: "User defined (ideal system)",
        },
    },
}

__HVAC_Device = {
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
            1: "Mechanical ventilation unit",
            3: "Boiler",
        },
    },
}


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
