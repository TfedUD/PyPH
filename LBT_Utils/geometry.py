# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for working with Ladybug-Tools objects"""

import ladybug_geometry.geometry3d.face


def LBT_geometry_dict_util(_dict):
    # type (dict): -> Optional[ladybug_geometry.geometry3d.face.Face3D]
    """Utility for de-serializing Ladybug Geometry dictionaries

    Arguments:
    ----------
        * _dict (dict): The dictionary for the object to try and convert to live
            LBT Geometry Object(s)

    Returns:
    --------
        * Optional[ladybug_geometry.geometry3d.face.Face3D]: The Ladybug Face3D Object
    """

    object_type = _dict.get("type", None)
    assert object_type is not None, (
        'Error converting to LBT Geometry: No "type" '
        "information found in the input dictionary?"
    )

    if str(object_type) == "Face3D":
        new_obj = ladybug_geometry.geometry3d.face.Face3D.from_dict(_dict)
    else:
        new_obj = None
        raise Exception(
            'Error: Cannot convert LBT Geometry of type: "{}"'.format(str(object_type))
        )

    return new_obj
