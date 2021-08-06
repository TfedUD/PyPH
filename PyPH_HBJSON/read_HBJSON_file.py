# -*- coding: utf-8 -*-
"""Functions for importing / translating Honeybee Models into WUFI-JSON """

import json

import honeybee.dictutil as hb_dict_util
import honeybee_energy.dictutil as energy_dict_util
import honeybee_radiance.dictutil as radiance_dict_util

# -------------------------------------------------------------------------------
def read_hb_json(_file_address: str) -> list:
    """Read in the HB_JSON from the Rhino File and convert back into HB Objects

    Arguments:
    ----------
        _file_address (str): A valid file path for the 'HB_Json' file to read

    Returns:
    --------
        (list): A list of the HB Object(s), rebuilt from the input JSON
    """

    # Note: cann't check this using str path, cus Mac OS vs. Windows OS, etc...
    # if not os.path.isfile(_file_address):
    #     raise Exception(f"The HB JSON file {_file_address} can not be found?")

    with open(_file_address) as json_file:
        data = json.load(json_file)

        try:
            hb_objs = hb_dict_util.dict_to_object(
                data, False
            )  # re-serialize as a core object
            if hb_objs is None:
                # try to re-serialize it as an energy object
                hb_objs = energy_dict_util.dict_to_object(data, False)
                if hb_objs is None:
                    # try to re-serialize it as a radiance object
                    hb_objs = radiance_dict_util.dict_to_object(data, False)
        except ValueError:
            # no 'type' key; assume that its a group of objects
            hb_objs = []
            for hb_dict in data.values():
                hb_obj = hb_dict_util.dict_to_object(
                    hb_dict, False
                )  # re-serialize as a core object
                if hb_obj is None:
                    # try to re-serialize it as an energy object
                    hb_obj = energy_dict_util.dict_to_object(hb_dict, False)
                    if hb_obj is None:
                        # try to re-serialize it as a radiance object
                        hb_obj = radiance_dict_util.dict_to_object(hb_dict, False)
                hb_objs.append(hb_obj)

        return hb_objs
