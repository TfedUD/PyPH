# -*- coding: utf-8 -*-
"""Functions used to build WUFI Zones and WUFI Rooms based on HB-Model inputs"""

import honeybee.room
import PHX.variant
import PHX.spaces
import PHX.utilization_patterns
import LBT_Utils.program

#-- Zones
#-------------------------------------------------------------------------------
def create_zone_from_HB_room( _hb_room: honeybee.room.Room ) -> PHX.variant.Zone:
    """Creates a new Zone from a single Honeybee 'Room'.

    Note: This function does not create the 'Spaces' within the Zone. Use
    create_PHX_Zones.add_Spaces_from_HB_room() in order to add Spaces if desired.
    
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

def set_Space_ventilation_from_HB_room( _hb_room, _phx_Space ):
    """Calcs and sets Space's ventilation flow rates based on the host Honeyebee Room"""

    #- Ventilation Airflow
    total_vent_airflow = LBT_Utils.program.calc_HB_Room_total_ventilation_m3sec( _hb_room )

    _phx_Space.ventilation.supply = total_vent_airflow * 3600
    _phx_Space.ventilation.extract = total_vent_airflow * 3600
    _phx_Space.ventilation.transfer = 0.0

def create_Spaces_from_HB_room(_hb_room):
    # type: (honeybee.room.Room) -> list[PHX.spaces.Space]
    """Returns a list of new Spaces based on the Honeybee Room"""

    #--- Get any detailed user-determined Space info on the HB-Room
    user_determined_space_dict = _hb_room.user_data.get('phx', {}).get('spaces', [])

    spaces = []
    if user_determined_space_dict:
        #--- Build new Spaces based on the User-determiend detailed inputs
        for space_dict in user_determined_space_dict.values():
            new_phx_space = PHX.spaces.Space.from_dict( space_dict )
            
            set_Space_ventilation_from_HB_room(_hb_room, new_phx_space)
        spaces.append( new_phx_space )
    else:
        #--- Build a default space if no detailed ones provided
        new_phx_space = PHX.spaces.Space()
        new_phx_space.space_number = None
        new_phx_space.space_name = f'{_hb_room.display_name}_room'
        
        set_Space_ventilation_from_HB_room(_hb_room, new_phx_space)
    spaces.append( new_phx_space )
    
    return spaces

def add_default_res_appliance_to_zone( _wp_zone: PHX.variant.Zone) -> PHX.variant.Zone:
    return None
    dw = Appliance_KitchenDishwasher()
    _wp_zone.add_new_appliance( dw )

    return _wp_zone


