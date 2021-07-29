"""Functions used to build WUFI Zones and WUFI Rooms based on HB-Model inputs"""

from honeybee.room import Room
from PHX.variant import Zone, WP_Room
from PHX.spaces import Space

#-- Zones
#-------------------------------------------------------------------------------
def create_zone_from_HB_room( _hb_room: Room ) -> Zone:
    """Creates a new Zone from a single Honeybee 'Room'
    
    Arguments:
    ----------
        * _hb_room (Room): The Honeybee room to use as the source for the new Zone

    Returns:
    --------
        * (Zone): The new Zone object with Attributes based on the Honeybee Room
    """
    
    zone = Zone()
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

def add_default_WP_room_from_HB_room( _wp_zone: Zone, _hb_room: Room) -> Zone:
    """

    Arguments:
    ----------
        * _wp_zone (Zone):
        * _hb_room (Room):

    Returns:
    --------
        * (Zone)

    """

    new_room = WP_Room()
    new_room.n = f'{_hb_room.display_name}_room'
    new_room.idUPatV = 1

    _wp_zone.add_new_WP_room( new_room )
    
    return _wp_zone

def add_detailed_WP_rooms_from_HB_room( _wp_zone: Zone, _hb_room: Room) -> Zone:
    """Sets the Zone's WP_Rooms based on detailed room data found in the 
    Honyebee room.user_data['phx']['spaces'] dictionary.
    
    """

    honeybee_spaces = _hb_room.user_data.get('phx', {}).get('spaces', {})
    for room_dict in honeybee_spaces.values():
        phx_space = Space.from_dict( room_dict )

        new_ph_room = WP_Room()

        _wp_zone.add_new_WP_room( new_ph_room )
    
    return _wp_zone

def add_default_res_appliance_to_zone( _wp_zone: Zone) -> Zone:
    return None
    dw = Appliance_KitchenDishwasher()
    _wp_zone.add_new_appliance( dw )

    return _wp_zone


