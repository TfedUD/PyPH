import Grasshopper.Kernel as ghK

import PHX.appliances
import PyPH_Rhino.gh_utils

# --
import PyPH_GH._component_info_

reload(PyPH_GH._component_info_)
ghenv.Component.name = "PyPH - Appliance"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev="SEP_13_2021")

if DEV:
    reload(PHX.appliances)
    reload(PyPH_Rhino.gh_utils)


def setup_component_input(_type_num):
    """Dynamic setup of the Component inputs based on the 'type' selector"""
    direction = (
        'Please input a valid Floor Type into "_type". Input either:\n'
        "    1-Dishwasher\n"
        "    2-Clothes Washer\n"
        "    3-Clothes Dryer\n"
        "    4-Refrigerator\n"
        "    5-Freezer\n"
        "    6-Combo Fridge / Freezer\n"
        "    7-Cooktop\n"
    )

    # Setup Inputs based on type
    input_nodes = {
        # -- Dishwasher
        1: {
            9: {"name": "_dishwasher_capacity_type", "desc": "(str)"},
            10: {"name": "_dishwasher_capacity", "desc": "(float)"},
            11: {"name": "_dishwasher_water_connection", "desc": "(str)"},
        },
        # -- Clothes Washer
        2: {
            9: {"name": "_clothes_washer_capacity", "desc": "(float)"},
            10: {"name": "_clothes_washer_modified_energy_factor", "desc": "(float)"},
            11: {"name": "_clothes_washer_water_connection", "desc": "(str)"},
            12: {"name": "_clothes_washer_utilization_factor", "desc": "(float)"},
        },
        # -- Clothes Dryer
        3: {
            9: {"name": "_clothes_dryer_type", "desc": "(str)"},
            10: {"name": "_clothes_dryer_gas_consumption", "desc": "(str)"},
            11: {"name": "_clothes_dryer_gas_efficiency_factor", "desc": "(float)"},
            12: {"name": "_clothes_dryer_utilization_factor", "desc": "(float)"},
        },
        # -- Fridge
        4: {},
        # -- Freezer
        5: {},
        # -- Combo Fridge, Freezer
        6: {},
        # -- Cooktop
        7: {
            9: {"name": "_cooktop_type", "desc": "(str)"},
        },
    }

    try:
        type_num = [int(s) for s in str(_type_num).split() if s.isdigit()][0]
        inputs = input_nodes.get(_type_num, {})
    except IndexError:
        inputs = {}
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, direction)

    for inputNum in range(9, 13):
        item = inputs.get(inputNum, {"name": "-", "desc": "-"})

        ghenv.Component.Params.Input[inputNum].NickName = item.get("name")
        ghenv.Component.Params.Input[inputNum].name = item.get("name")
        ghenv.Component.Params.Input[inputNum].Description = item.get("desc")

    return None


def get_input_values():
    """Dynamic Component Input 'get' - pulls all the input names/values into a dictionary"""

    inputs = {}

    for input in ghenv.Component.Params.Input:
        try:
            vals = list(input.VolatileData[0])
            try:
                val = float(str(vals[0]))
            except:
                val = str(vals[0])
            inputs[input.Name] = val

        except Exception as e:
            inputs[input.Name] = None

    return inputs


def validate_input(_attr_name, _input_val):
    if _attr_name is None or _input_val is None:
        return None, None

    # -------------------------------------------------------------------------------
    # --- For remapping GH_Component Keys to the Appliance Class Attributes
    key_map = {
        # -- Basics
        "_type": {"PHX_name": "type", "type": "int"},
        "comment_": {"PHX_name": "comment", "type": "str"},
        "quantity_": {"PHX_name": "quantity", "type": "float"},
        "in_conditioned_space_": {"PHX_name": "in_conditioned_space", "type": "bool"},
        "energy_ref_norm_": {"PHX_name": "reference_energy_norm", "type": "str"},
        "energy_demand_yr_": {"PHX_name": "energy_demand", "type": "float"},
        "energy_demand_use_": {"PHX_name": "energy_demand_per_use", "type": "float"},
        "combined_energy_factor_": {"PHX_name": "combined_energy_facor", "type": "float"},
        # -- Dishwasher
        "_dishwasher_capacity_type": {"PHX_name": "dishwasher_capacity_type", "type": "int"},
        "_dishwasher_capacity": {"PHX_name": "dishwasher_capacity", "type": "float"},
        "_dishwasher_water_connection": {"PHX_name": "dishwasher_water_connection", "type": "int"},
        # -- Laundry Washer
        "_clothes_washer_capacity": {"PHX_name": "washer_capacity", "type": "float"},
        "_clothes_washer_modified_energy_factor": {"PHX_name": "washer_modified_energy_factor", "type": "float"},
        "_clothes_washer_water_connection": {"PHX_name": "washer_connection", "type": "int"},
        "_clothes_washer_utilization_factor": {"PHX_name": "washer_utilization_factor", "type": "float"},
        # -- Laundry Dryer
        "_clothes_dryer_type": {"PHX_name": "dryer_type", "type": "int"},
        "_clothes_dryer_gas_consumption": {"PHX_name": "dryer_gas_consumption", "type": "float"},
        "_clothes_dryer_gas_efficiency_factor": {"PHX_name": "dryer_gas_efficiency_factor", "type": "float"},
        "_clothes_dryer_utilization_factor_type": {"PHX_name": "dryer_field_utilization_factor_type", "type": "int"},
        "_clothes_dryer_utilization_factor": {"PHX_name": "dryer_field_utilization_factor", "type": "float"},
        # -- Cooktop
        "_cooktop_type": {"PHX_name": "cooktop_type", "type": "int"},
        # -- PHIUS Lighting
        "_lighting_frac_high_efficiency": {"PHX_name": "lighting_frac_high_efficiency", "type": "float"},
        "_user_defined_total": {"PHX_name": "user_defined_total", "type": "float"},
    }

    # -- Get the Input value
    validation_schema = key_map.get(_attr_name, None)
    if validation_schema is None:
        return None, None

    phx_attr_name = validation_schema.get("PHX_name")

    # -- Check the Type of the input value
    type_name = validation_schema.get("type", "str")
    try:
        if type_name == "str":
            input_value = str(_input_val)
        elif type_name == "int":
            input_value = int(_input_val)
        elif type_name == "float":
            input_value = float(_input_val)
        elif type_name == "bool":
            input_value = bool(_input_val)
        else:
            raise Exception
    except Exception as e:
        msg = 'Error: Input value "{}" [{}] not allowed for input: "{}". Provide only "{}" values.'.format(
            _input_val, type(_input_val), _attr_name, type_name
        )
        raise Exception(msg)

    return (phx_attr_name, input_value)


# -------------------------------------------------------------------------------
# Set all the component input values / names / hints

setup_component_input(_type)
ghenv.Component.Attributes.Owner.OnPingDocument()


if _type:
    inputs = get_input_values()

    # -- The new Appliance
    appliance_ = PHX.appliances.Appliance()

    # -- Set all the attributes of the new Appliance
    for k, v in inputs.items():
        k, v = validate_input(k, v)
        if k is None or v is None:
            continue

        setattr(appliance_, k, v)

PyPH_Rhino.gh_utils.object_preview(appliance_)
