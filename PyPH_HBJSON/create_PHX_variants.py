# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions to create PHX Materiala, Assembly-Layers, and Construction Assemblies from HB-JSON"""

import honeybee.room
import PHX.variant
import PHX.project


def get_host_variant(
    _project: PHX.project.Project, _hb_room: honeybee.room.Room
) -> PHX.variant.Variant:
    """Returns the HB Room's Host Variant. Will create a new variant
    based on the id/name info found on the HB Room user_data.

    If none is found, returns the Default variant for the projecg
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
