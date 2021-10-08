RELEASE_VERSION = "PyPH v0.1"
CATEGORY = "PH-Tools"


class ComponentNameError(Exception):
    def __init__(self, _name, error):
        self.message = 'Error: Cannot get Component Params for: "{}"'.format(_name)
        print(error)
        super(ComponentNameError, self).__init__(self.message)


sub_catagories = {
    4: "04 | PHX Model",
    5: "05 | Temp",
    6: "06 | Temp",
}

component_params = {
    "PyPH - Get PHIUS Program": {
        "NickName": "Get PHIUS Program",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - PHIUS Certification": {
        "NickName": "PHIUS Certification",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Create Bldg Segment": {
        "NickName": "PHX Bldg Segment",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Zone Occupancy": {
        "NickName": "PHX Zone Occupancy",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - PHIUS MF Calculator": {
        "NickName": "PHIUS MF Calculator",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Appliance": {
        "NickName": "PHX Appliance",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Appliance Set": {
        "NickName": "PHX Appliance Set",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Non-Res Program": {
        "NickName": "PHX Non-Res. Program",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    # ---------------------------------------------------------------------------
    # Section 01.1 | Geometry
    "PyPH - Get Surface Params": {
        "NickName": "Get Surface Params",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Airtightness": {
        "NickName": "PHX Airtightness",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Create PHX Spaces": {
        "NickName": "PHX Spaces",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    # ---------------------------------------------------------------------------
    # Section 01.XX | Ventilation
    "PyPH - Ventilation System": {
        "NickName": "PHX Ventilation System",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Ventilation Duct": {
        "NickName": "PHX Duct",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Ventilation Unit": {
        "NickName": "PHX Ventilator",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Summer Ventilation": {
        "NickName": "PHX Summer Ventilation",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    # ---------------------------------------------------------------------------
    # Section 01.XX | Loads
    "PyPH - Load Lighting": {
        "NickName": "PHX Lighting",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    # ---------------------------------------------------------------------------
    # Section 01.1 | Schedules
    "PyPH - Sched Occupancy": {
        "NickName": "PHX Sched: Occupancy",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Sched Lighting": {
        "NickName": "PHX Sched: Lighting",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
    "PyPH - Sched Ventilation": {
        "NickName": "PHX Sched: Ventilation",
        "Message": RELEASE_VERSION,
        "Category": CATEGORY,
        "SubCategory": 4,
    },
}


def set_component_params(ghenv, dev=False):
    # type (ghenv, Optional[str | bool]) -> None
    """
    Sets the visible attributes of the Grasshopper Component (Name, Date, etc..)

    Args:
        ghenv: The Grasshopper Component 'ghenv' variable
        dev: (str | bool) Default=False. If False, will use the RELEASE_VERSION value as the
            'message' shown on the bottom of the component in the Grasshopper
            scene.
            If a string is passed in, will use that for the 'message'
            shown instead.
    """
    try:
        compo_name = ghenv.Component.Name
        sub_cat_num = component_params.get(compo_name).get("SubCategory")
        sub_cat_name = sub_catagories.get(sub_cat_num)
    except Exception as e:
        raise ComponentNameError(compo_name, e)

    # ------ Set the visible message
    if dev:
        msg = "DEV | {}".format(str(dev))
    else:
        msg = component_params.get(compo_name).get("Message")

    ghenv.Component.Message = msg

    # ------ Set the othere stuff
    ghenv.Component.NickName = component_params.get(compo_name).get("NickName")
    ghenv.Component.Category = CATEGORY
    ghenv.Component.SubCategory = sub_cat_name
    ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
