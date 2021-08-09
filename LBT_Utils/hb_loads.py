# -*- coding: utf-8 -*-
"""Utility functions pulled from Honeybee 'ApplyLoadVals' Grasshopper component"""


def dup_load(hb_obj, object_name, object_class, always_on=True):
    """Duplicate a load object assigned to a Room or ProgramType."""

    # -- try to get the load object assgined to the Room or ProgramType
    try:
        # -- assume it's a Room
        load_obj = hb_obj.properties
        for attribute in ("energy", object_name):
            load_obj = getattr(load_obj, attribute)
    except AttributeError:
        # -- it's a ProgramType
        load_obj = getattr(hb_obj, object_name)

    load_id = "{}_{}".format(hb_obj.identifier, object_name)
    try:
        # -- duplicate the load object
        dup_load = load_obj.duplicate()
        dup_load.identifier = load_id
        return dup_load
    except AttributeError:
        # -- create a new object
        try:
            # -- assume it's People, Lighting, Equipment or Infiltration
            return object_class(load_id, 0, always_on)
        except:
            # -- it's a Ventilation object
            return object_class(load_id)


def assign_load(hb_obj, load_obj, object_name):
    """Assign a load object to a Room or a ProgramType."""

    try:
        # -- assume it's a Room
        setattr(hb_obj.properties.energy, object_name, load_obj)
    except AttributeError:
        # -- it's a ProgramType
        setattr(hb_obj, object_name, load_obj)
