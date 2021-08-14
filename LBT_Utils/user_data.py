# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for working with Ladybug-Tools objects"""

from copy import deepcopy
from collections import defaultdict
import honeybee


def add_to_HB_Obj_user_data(_hb_obj, _dict={}, _key="phx", _write_mode="update"):
    # type: ( honeybee, dict, str, str ) -> honeybee
    """Adds the a new dictionary entry to the Honeybee Object's 'user_data'

    Arguments:
    ----------
        * _hb_obj (): The Honeybee Object to add the new dict entry to
        * _key (str): The 'key' to use for the new dict entry. Default='phx' which
            is the 'top' layer of the Honeybee Object's user_data dictionary
        * _dict (dict): The dict entry to add to the Honeybee Object.
        * _write_mode (str): 'update' or 'overwrite'. The way to add the new dict
            entry to the Honeybee object's user_data. Default='update'

    Returns:
    --------
        * Honeybee Object: The Input HB Object with its 'user_data' updated

    """

    new_user_data = deepcopy(_hb_obj.user_data)
    if not isinstance(new_user_data, dict):
        new_user_data = {}

    if "phx" not in new_user_data:
        new_user_data["phx"] = defaultdict(dict)

    if _write_mode == "update":
        if _key == "phx":
            new_user_data["phx"].update(_dict)
        else:
            new_user_data["phx"][_key].update(_dict)
    elif _write_mode == "overwrite":
        if _key == "phx":
            new_user_data["phx"] = _dict
        else:
            new_user_data["phx"][_key] = _dict

    _hb_obj.user_data = new_user_data

    return _hb_obj
