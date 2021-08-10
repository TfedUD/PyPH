# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to create PHX Materiala, Assembly-Layers, and Construction Assemblies from HB-JSON"""

import honeybee.room
import PHX.variant
import PHX.project


def get_host_PHX_Variant(
    _project: PHX.project.Project, _hb_room: honeybee.room.Room
) -> PHX.variant.Variant:
    """Returns a Honybee Room's Host PHX-Variant.

    Will first look for the Honeybee.room.Room.user_data['phx']['variants_id'] to
    get a name/id for the PHX-Variant. If name/id is found, will create a new variant
    with that id if none already exists on the PHX.project.Project object.

    If none is found (this attribute wasn't set by the
    user), will return the PHX.project.Project's default-variant.

    Arguments:
    ----------
        * _project (PHX.project.Project): The PHX-Project Object.
        * _ hb_room (honeybee.room.Room): The Honeybee Room to use as the source.

    Returns:
    --------
        * (PHX.variant.Variant): The Honeybee Room's host PHX-Variant.
    """

    var_ident = (
        _hb_room.user_data.get("phx", {}).get("variant_id", {}).get("identifier")
    )
    var_id = _hb_room.user_data.get("phx", {}).get("variant_id", {}).get("id")
    var_name = _hb_room.user_data.get("phx", {}).get("variant_id", {}).get("name")

    if not var_ident:
        host_variant = PHX.variant.Variant.default()
    else:
        host_variant = _project.get_variant_by_identifier(var_ident)

        if not host_variant:
            host_variant = PHX.variant.Variant()
            host_variant.identifier = var_ident
            host_variant.id = var_id
            host_variant.n = var_name

    _project.add_variant(host_variant)

    return host_variant
