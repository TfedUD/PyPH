# -*- coding: utf-8 -*-
"""Functions used to build WUFI Zones and WUFI Rooms based on HB-Model inputs"""

import honeybee.room
import PHX.variant
import PHX.spaces

#-- Zones
#-------------------------------------------------------------------------------
def create_zone_from_HB_room( _hb_room: honeybee.room.Room ) -> PHX.variant.Zone:
    """Creates a new Zone from a single Honeybee 'Room'
    
    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee room to use as the source for the new Zone

    Returns:
    --------
        * (Zone): The new Zone object with Attributes based on the Honeybee Room
    """
    
    zone = PHX.variant.Zone()
    zone.n = _hb_room.display_name
    zone.identifier = _hb_room.identifier
    zone.source_zone_identifiers.append( _hb_room.identifier)
    
    if _hb_room.volume:
        zone.volume_gross = _hb_room.volume
        zone.volume_gross_selection = 7 #User defined
        zone.volume_net_selection = 4 #Estimated from gross volume
        
    if _hb_room.floor_area:
        zone.floor_area = _hb_room.floor_area
        zone.floor_area_selection = 6 # User Determined

    return zone

def add_default_Space_from_HB_room( _phx_Zone: PHX.variant.Zone, _hb_room: honeybee.room.Room) -> PHX.variant.Zone:
    """Create a new default Space object for a HB Room. This is used if no detailed
    Space information is supplied by the user. By default, each Honyebee Room will have a single 'Space.'

    Arguments:
    ----------
        * _phx_Zone (PHX.variant.Zone): The PHX.Zone Object to serve as the 'host'
            for the new PHX.spaces.Space
        * _hb_room (honeybee.room.Room): The source Honeybee 'Room' to use to set the name for
            the new PHX.spaces.Space created.

    Returns:
    --------
        * (PHX.variant.Zone): The input PHX.variant.Zone with the new PHX.spaces.Space 
            now as a 'child' of the Zone.
    """

    new_space = PHX.spaces.Space()
    new_space.space_number = None
    new_space.space_name = f'{_hb_room.display_name}_room'
    # new_space.idUPatV = 1

    _phx_Zone.add_new_space( new_space )
    
    return _phx_Zone

def add_detailed_Spaces_from_HB_room( _phx_Zone: PHX.variant.Zone, _hb_room: honeybee.room.Room) -> PHX.variant.Zone:
    """Sets the Zone's Spaces based on detailed Space data found in the 
    Honyebee room.user_data['phx']['spaces'] dictionary.

    Arguments:
    ----------
        * _phx_Zone (PHX.variant.Zone): The PHX.Zone Object to serve as the 'host'
            for the new PHX.spaces.Space
        * _hb_room (honeybee.room.Room): The source Honeybee 'Room' to use to set the name for
            the new PHX.spaces.Space created.

    Returns:
    --------
        * (PHX.variant.Zone): The input PHX.variant.Zone with the new PHX.spaces.Space 
            now as a 'child' of the Zone.
    """

    honeybee_spaces = _hb_room.user_data.get('phx', {}).get('spaces', {})
    for room_dict in honeybee_spaces.values():

        phx_space = PHX.spaces.Space.from_dict( room_dict )

        _phx_Zone.add_new_space( phx_space )
    
    return _phx_Zone

def add_default_res_appliance_to_zone( _wp_zone: PHX.variant.Zone) -> PHX.variant.Zone:
    return None
    dw = Appliance_KitchenDishwasher()
    _wp_zone.add_new_appliance( dw )

    return _wp_zone


