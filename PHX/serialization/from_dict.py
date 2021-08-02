# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
Functions for converting text dictionaries to PHX Objects. These functions are passed 
to the Object when it is instantiated in order to avoide circular reference problems since 
certain functions use other PHX Object to_dict() constructors (ie: _Floor).
"""

# from ..geometry import LBT_geometry_dict_util
import PHX
import PHX.geometry

def _FloorSegment(_cls, _input_dict):
    new_obj = _cls()

    new_obj.weighting_factor = _input_dict.get('weighting_factor')
    new_obj.floor_area_gross = _input_dict.get('floor_area_gross')
    new_obj.space_name = _input_dict.get('space_name')
    new_obj.space_number = _input_dict.get('space_number')
    new_obj.non_res_lighting = _input_dict.get('non_res_lighting')
    new_obj.non_res_motion = _input_dict.get('non_res_motion')
    new_obj.non_res_usage = _input_dict.get('non_res_usage')
    new_obj.ventilation_v_sup = _input_dict.get('ventilation_v_sup')
    new_obj.ventilation_v_eta = _input_dict.get('ventilation_v_eta')
    new_obj.ventilation_v_trans = _input_dict.get('ventilation_v_trans')
    new_obj.host_zone_identifier = _input_dict.get('host_zone_identifier')

    for _ in _input_dict.get('geometry', {}).values():
        new_obj.geometry.append(PHX.geometry.LBT_geometry_dict_util(_))

    return new_obj

def _Floor(_cls, _input_dict):
    new_obj = _cls()
        
    new_obj.space_name = _input_dict.get('space_name')
    new_obj.space_number = _input_dict.get('space_number')
    new_obj.non_res_lighting = _input_dict.get('non_res_lighting')
    new_obj.non_res_motion = _input_dict.get('non_res_motion')
    new_obj.non_res_usage = _input_dict.get('non_res_usage')
    new_obj.ventilation_v_sup = _input_dict.get('ventilation_v_sup')
    new_obj.ventilation_v_eta = _input_dict.get('ventilation_v_eta')
    new_obj.ventilation_v_trans = _input_dict.get('ventilation_v_trans')
    new_obj.host_zone_identifier = _input_dict.get('host_zone_identifier')

    new_obj.floor_segments = []
    for flr_seg_dict in _input_dict.get('floor_segments', {}).values():
        if flr_seg_dict:
            new_flr_seg = PHX.spaces.FloorSegment.from_dict(flr_seg_dict)
            new_obj.floor_segments.append( new_flr_seg )

    return new_obj

def _Volume(_cls, _input_dict):
    new_obj = _cls()

    new_obj.space_name = _input_dict.get('space_name')
    new_obj.space_number = _input_dict.get('space_number')
    new_obj.host_zone_identifier = _input_dict.get('host_zone_identifier')
    new_obj._average_ceiling_height = _input_dict.get('_average_ceiling_height')
    new_obj._volume = _input_dict.get('_volume')
    
    floor_dict = _input_dict.get('floor')
    if floor_dict:
        new_obj.floor = PHX.spaces.Floor.from_dict(floor_dict)

    new_obj.volume_geometry= []
    for _ in _input_dict.get('volume_geometry', {}).values():
        new_geom_list = []
        for __ in _.values():
            new_geom_list.append( PHX.geometry.LBT_geometry_dict_util(__) )
        new_obj.volume_geometry.append(new_geom_list)

    return new_obj

def _Space(_cls, _input_dict):
    new_obj = _cls()

    new_obj.space_name = _input_dict.get('space_name')
    new_obj.space_number = _input_dict.get('space_number')
    new_obj.host_zone_identifier = _input_dict.get('host_zone_identifier')
    new_obj.occupancy = _input_dict.get('occupancy')
    new_obj.equipment = _input_dict.get('equipment')
    new_obj.ventilation = _input_dict.get('ventilation')

    new_obj.volumes = []
    for volume_dict in _input_dict.get('volumes', {}).values():
        new_obj.volumes.append( PHX.spaces.Volume.from_dict(volume_dict) )

    return new_obj