# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
Functions for converting PHX Objects to serializable text dictionaries. All PHX Objects
should be able to be converted to fully text represenations.
"""

def _FloorSegment(_obj):
    d = {}  

    d.update( { 'weighting_factor': _obj.weighting_factor }  )
    d.update( { 'floor_area_gross': _obj.floor_area_gross }  )
    d.update( { 'space_name': _obj.space_name }  )
    d.update( { 'space_number': _obj.space_number }  )
    d.update( { 'non_res_lighting': _obj.non_res_lighting }  )
    d.update( { 'non_res_motion': _obj.non_res_motion }  )
    d.update( { 'non_res_usage': _obj.non_res_usage }  )
    d.update( { 'ventilation_v_sup': _obj.ventilation_v_sup }  )
    d.update( { 'ventilation_v_eta': _obj.ventilation_v_eta }  )
    d.update( { 'ventilation_v_trans': _obj.ventilation_v_trans }  )
    d.update( { 'host_zone_identifier': _obj.host_zone_identifier }  )
    
    geometry_dict = {}
    for _ in _obj.geometry:
        geometry_dict.update( { id(_): _.to_dict() } )
    d.update( { 'geometry': geometry_dict }  )

    return d 

def _Floor(_obj):
    d = {}

    d.update( { 'space_name': _obj.space_name }  )
    d.update( { 'space_number': _obj.space_number }  )
    d.update( { 'non_res_lighting': _obj.non_res_lighting }  )
    d.update( { 'non_res_motion': _obj.non_res_motion }  )
    d.update( { 'non_res_usage': _obj.non_res_usage }  )
    d.update( { 'ventilation_v_sup': _obj.ventilation_v_sup }  )
    d.update( { 'ventilation_v_eta': _obj.ventilation_v_eta }  )
    d.update( { 'ventilation_v_trans': _obj.ventilation_v_trans }  )
    d.update( { 'host_zone_identifier': _obj.host_zone_identifier }  )

    floor_segments_dict = {}
    for flr_seg in _obj.floor_segments:
        floor_segments_dict.update( { id(flr_seg): flr_seg.to_dict() } )
    d.update( { 'floor_segments': floor_segments_dict }  )

    return d

def _Volume(_obj):
    d = {}

    d.update( { 'space_name': _obj.space_name }  )
    d.update( { 'space_number': _obj.space_number }  )
    d.update( { 'host_zone_identifier': _obj.host_zone_identifier }  )
    d.update( { '_average_ceiling_height': _obj._average_ceiling_height }  )
    d.update( { '_volume': _obj._volume }  )
    
    d.update( { 'floor': _obj.floor.to_dict() }  )

    volume_geometry_dict = {}
    for list_of_geom in _obj.volume_geometry:
        geom_list = {}
        for geom in list_of_geom:
            geom_list.update( { id(geom): geom.to_dict() } )
        volume_geometry_dict.update( { id(geom_list):geom_list } )

    d.update( { 'volume_geometry': volume_geometry_dict }  )

    return d

def _Space(_obj):
    d = {}

    d.update( { 'space_name': _obj.space_name }  )
    d.update( { 'space_number': _obj.space_number }  )
    d.update( { 'host_zone_identifier': _obj.host_zone_identifier }  )
    d.update( { 'occupancy': _obj.occupancy }  )
    d.update( { 'equipment': _obj.equipment }  )
    d.update( { 'ventilation': _obj.ventilation }  )

    volumes_dict = {}
    for volume in _obj.volumes:
        volumes_dict.update( { id(volume):volume.to_dict() } )
    d.update( { 'volumes': volumes_dict }  )

    return d